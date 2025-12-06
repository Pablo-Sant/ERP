# api/fi_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc
from typing import List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
from fastapi.responses import JSONResponse

from core.database import get_db
from api.auth import get_current_user
from models.usuario import UsuarioModel

# Models Financeiro
from models.financeiro_conta import FinanceiroContas
from models.financeiro_lancamentos import FinanceiroLancamentos
from models.financeiro_extrato import FinanceiroExtratosBancarios
from models.financeiro_orcamento import FinanceiroOrcamentos
from models.financeiro_fluxo_caixa import FinanceiroFluxoCaixa
from models.financeiro_conciliacoes import FinanceiroConciliacoes
from models.contabilidade_plano_conta import ContabilidadePlanoContas
from models.contabilidade_lancamento import ContabilidadeLancamentos
from models.fiscal_notas_fiscais import FiscalNotasFiscais
from models.fiscal_impostos import FiscalImpostos

# Schemas Financeiro
from schemas.financeiro_contas_financeiras import (
    FinanceiroContasCreate, FinanceiroContasResponse, FinanceiroContasUpdate
)
from schemas.financeiro_lancamentos_financeiros import (
    FinanceiroLancamentosCreate, FinanceiroLancamentosResponse, FinanceiroLancamentosUpdate
)
from schemas.financeiro_extratos_bancarios import (
    FinanceiroExtratosBancariosCreate, FinanceiroExtratosBancariosResponse, FinanceiroExtratosBancariosUpdate
)
from schemas.financeiro_orcamentos import (
    FinanceiroOrcamentosCreate, FinanceiroOrcamentosResponse, FinanceiroOrcamentosUpdate
)
from schemas.financeiro_fluxo_caixa import (
    FinanceiroFluxoCaixaCreate, FinanceiroFluxoCaixaResponse, FinanceiroFluxoCaixaUpdate
)
from schemas.financeiro_conciliacoes import (
    FinanceiroConciliacoesCreate, FinanceiroConciliacoesResponse, FinanceiroConciliacoesUpdate
)
from schemas.contabilidade_plano_conta import (
    ContabilidadePlanoContasCreate, ContabilidadePlanoContasResponse, ContabilidadePlanoContasUpdate
)
from schemas.contabilidade_lancamentos_contabeis import (
    ContabilidadeLancamentosCreate, ContabilidadeLancamentosResponse, ContabilidadeLancamentosUpdate
)
from schemas.fiscal_notas_fiscais import (
    FiscalNotasFiscaisCreate, FiscalNotasFiscaisResponse, FiscalNotasFiscaisUpdate
)
from schemas.fiscal_impostos import (
    FiscalImpostosCreate, FiscalImpostosResponse, FiscalImpostosUpdate
)

router = APIRouter(prefix="/fi", tags=["Financeiro"])

# ========== CONTAS FINANCEIRAS ==========

@router.get("/contas")
async def listar_contas_fix(
    db: AsyncSession = Depends(get_db),
    tipo: Optional[str] = Query(None),
    ativo: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    # current_user: UsuarioModel = Depends(get_current_user)  # COMENTE TEMPORARIAMENTE
):
    """
    Rota /contas CORRIGIDA - Versão simplificada que funciona
    """
    try:
        print("=== /contas-fix chamada ===")
        
        from sqlalchemy import text
        
        # 1. Construir SQL
        sql = """
        SELECT 
            id_conta,
            nome,
            tipo,
            saldo_inicial,
            data_abertura,
            ativo
        FROM fi.financeiro_contas
        WHERE 1=1
        """
        
        params = {}
        
        if tipo:
            sql += " AND tipo = :tipo"
            params['tipo'] = tipo
            
        if ativo is not None:
            sql += " AND ativo = :ativo"
            params['ativo'] = ativo
            
        sql += " ORDER BY nome"
        sql += " LIMIT :limit OFFSET :skip"
        
        params['limit'] = limit
        params['skip'] = skip
        
        print(f"Executando SQL: {sql}")
        print(f"Parâmetros: {params}")
        
        # 2. Executar query
        result = await db.execute(text(sql), params)
        rows = result.fetchall()
        
        # 3. Formatar resposta
        contas = []
        for row in rows:
            conta = {
                "id_conta": row[0],
                "nome": row[1],
                "tipo": row[2],
                "saldo_inicial": float(row[3]) if row[3] else 0.0,
                "data_abertura": row[4].isoformat() if row[4] else None,
                "ativo": bool(row[5]) if row[5] is not None else True
            }
            contas.append(conta)
        
        print(f"Sucesso! Retornando {len(contas)} contas")
        return contas
        
    except Exception as e:
        print(f"ERRO em /contas-fix: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            "error": True,
            "message": str(e),
            "type": type(e).__name__
        }
    

@router.get("/contas/{conta_id}", response_model=FinanceiroContasResponse)
async def get_conta(
    conta_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Obtém uma conta financeira específica"""
    query = select(FinanceiroContas).where(FinanceiroContas.id_conta == conta_id)
    result = await db.execute(query)
    conta = result.scalar_one_or_none()
    
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada"
        )
    
    return conta

@router.post("/contas", response_model=FinanceiroContasResponse, status_code=status.HTTP_201_CREATED)
async def criar_conta(
    conta: FinanceiroContasCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria uma nova conta financeira"""
    try:
        # Verificar se já existe conta com mesmo nome
        query = select(FinanceiroContas).where(FinanceiroContas.nome == conta.nome)
        result = await db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe uma conta com este nome"
            )
        
        db_conta = FinanceiroContas(**conta.dict())
        db.add(db_conta)
        await db.commit()
        await db.refresh(db_conta)
        return db_conta
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar conta: {str(e)}"
        )

@router.put("/contas/{conta_id}", response_model=FinanceiroContasResponse)
async def atualizar_conta(
    conta_id: int,
    conta_update: FinanceiroContasUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Atualiza uma conta financeira existente"""
    query = select(FinanceiroContas).where(FinanceiroContas.id_conta == conta_id)
    result = await db.execute(query)
    db_conta = result.scalar_one_or_none()
    
    if not db_conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada"
        )
    
    update_data = conta_update.dict(exclude_unset=True)
    
    # Verificar duplicidade de nome
    if 'nome' in update_data:
        query = select(FinanceiroContas).where(
            FinanceiroContas.nome == update_data['nome'],
            FinanceiroContas.id_conta != conta_id
        )
        result = await db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe uma conta com este nome"
            )
    
    for field, value in update_data.items():
        setattr(db_conta, field, value)
    
    try:
        await db.commit()
        await db.refresh(db_conta)
        return db_conta
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar conta: {str(e)}"
        )

@router.delete("/contas/{conta_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_conta(
    conta_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Exclui uma conta financeira"""
    query = select(FinanceiroContas).where(FinanceiroContas.id_conta == conta_id)
    result = await db.execute(query)
    conta = result.scalar_one_or_none()
    
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada"
        )
    
    # Verificar se há lançamentos associados
    lancamentos_query = select(FinanceiroLancamentos).where(
        FinanceiroLancamentos.id_conta == conta_id
    )
    lancamentos_result = await db.execute(lancamentos_query)
    if lancamentos_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível excluir conta com lançamentos associados"
        )
    
    try:
        await db.delete(conta)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir conta: {str(e)}"
        )

# ========== LANÇAMENTOS FINANCEIROS ==========

@router.get("/lancamentos", response_model=List[FinanceiroLancamentosResponse])
async def listar_lancamentos(
    db: AsyncSession = Depends(get_db),
    conta_id: Optional[int] = Query(None),
    tipo: Optional[str] = Query(None),
    data_inicio: Optional[date] = Query(None),
    data_fim: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    # current_user: UsuarioModel = Depends(get_current_user)  # Comente temporariamente
):
    """Lista todos os lançamentos financeiros"""
    try:
        print("=== /lancamentos chamada ===")
        
        # Usar SQL direto para evitar problemas do ORM
        from sqlalchemy import text
        
        sql = """
        SELECT 
            id_lancamento,
            id_conta,
            descricao,
            tipo,
            valor,
            data_lancamento,
            created_at
        FROM fi.financeiro_lancamentos
        WHERE 1=1
        """
        
        params = {}
        
        if conta_id:
            sql += " AND id_conta = :conta_id"
            params['conta_id'] = conta_id
            
        if tipo:
            sql += " AND tipo = :tipo"
            params['tipo'] = tipo
            
        if data_inicio:
            sql += " AND data_lancamento >= :data_inicio"
            params['data_inicio'] = data_inicio
            
        if data_fim:
            sql += " AND data_lancamento <= :data_fim"
            params['data_fim'] = data_fim
            
        sql += " ORDER BY data_lancamento DESC"
        sql += " LIMIT :limit OFFSET :skip"
        
        params['limit'] = limit
        params['skip'] = skip
        
        print(f"Executando SQL: {sql}")
        print(f"Parâmetros: {params}")
        
        # Executar query
        result = await db.execute(text(sql), params)
        rows = result.fetchall()
        
        # Formatar resposta
        lancamentos = []
        for row in rows:
            lancamento = {
                "id_lancamento": row[0],
                "id_conta": row[1],
                "descricao": row[2],
                "tipo": row[3],
                "valor": float(row[4]) if row[4] else 0.0,
                "data_lancamento": row[5].isoformat() if row[5] else None,
                "created_at": row[6].isoformat() if row[6] else None
            }
            lancamentos.append(lancamento)
        
        print(f"Sucesso! Retornando {len(lancamentos)} lançamentos")
        return lancamentos
        
    except Exception as e:
        print(f"ERRO em /lancamentos: {str(e)}")
        import traceback
        traceback.print_exc()
        
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )

@router.get("/lancamentos/{lancamento_id}", response_model=FinanceiroLancamentosResponse)
async def get_lancamento(
    lancamento_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Obtém um lançamento financeiro específico"""
    query = select(FinanceiroLancamentos).where(FinanceiroLancamentos.id_lancamento == lancamento_id)
    result = await db.execute(query)
    lancamento = result.scalar_one_or_none()
    
    if not lancamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento não encontrado"
        )
    
    return lancamento

@router.post("/lancamentos", response_model=FinanceiroLancamentosResponse, status_code=status.HTTP_201_CREATED)
async def criar_lancamento(
    lancamento: FinanceiroLancamentosCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria um novo lançamento financeiro"""
    try:
        # Verificar se conta existe
        query = select(FinanceiroContas).where(FinanceiroContas.id_conta == lancamento.id_conta)
        result = await db.execute(query)
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Conta não encontrada"
            )
        
        db_lancamento = FinanceiroLancamentos(**lancamento.dict(), created_at=datetime.now())
        db.add(db_lancamento)
        await db.commit()
        await db.refresh(db_lancamento)
        return db_lancamento
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar lançamento: {str(e)}"
        )

@router.put("/lancamentos/{lancamento_id}", response_model=FinanceiroLancamentosResponse)
async def atualizar_lancamento(
    lancamento_id: int,
    lancamento_update: FinanceiroLancamentosUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Atualiza um lançamento financeiro existente"""
    query = select(FinanceiroLancamentos).where(FinanceiroLancamentos.id_lancamento == lancamento_id)
    result = await db.execute(query)
    db_lancamento = result.scalar_one_or_none()
    
    if not db_lancamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento não encontrado"
        )
    
    update_data = lancamento_update.dict(exclude_unset=True)
    
    # Verificar se conta existe se for atualizar
    if 'id_conta' in update_data:
        query = select(FinanceiroContas).where(FinanceiroContas.id_conta == update_data['id_conta'])
        result = await db.execute(query)
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Conta não encontrada"
            )
    
    for field, value in update_data.items():
        setattr(db_lancamento, field, value)
    
    try:
        await db.commit()
        await db.refresh(db_lancamento)
        return db_lancamento
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar lançamento: {str(e)}"
        )

@router.delete("/lancamentos/{lancamento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_lancamento(
    lancamento_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Exclui um lançamento financeiro"""
    query = select(FinanceiroLancamentos).where(FinanceiroLancamentos.id_lancamento == lancamento_id)
    result = await db.execute(query)
    lancamento = result.scalar_one_or_none()
    
    if not lancamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento não encontrado"
        )
    
    try:
        await db.delete(lancamento)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir lançamento: {str(e)}"
        )

# ========== EXTRATOS BANCÁRIOS ==========

@router.get("/extratos", response_model=List[FinanceiroExtratosBancariosResponse])
async def listar_extratos(
    db: AsyncSession = Depends(get_db),
    conta_id: Optional[int] = Query(None),
    tipo: Optional[str] = Query(None),
    conciliado: Optional[bool] = Query(None),
    data_inicio: Optional[date] = Query(None),
    data_fim: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista todos os extratos bancários"""
    query = select(FinanceiroExtratosBancarios)
    
    if conta_id:
        query = query.where(FinanceiroExtratosBancarios.id_conta == conta_id)
    if tipo:
        query = query.where(FinanceiroExtratosBancarios.tipo == tipo)
    if conciliado is not None:
        query = query.where(FinanceiroExtratosBancarios.conciliado == conciliado)
    if data_inicio:
        query = query.where(FinanceiroExtratosBancarios.data_movimento >= data_inicio)
    if data_fim:
        query = query.where(FinanceiroExtratosBancarios.data_movimento <= data_fim)
    
    query = query.offset(skip).limit(limit).order_by(desc(FinanceiroExtratosBancarios.data_movimento))
    
    result = await db.execute(query)
    extratos = result.scalars().all()
    return extratos

@router.post("/extratos", response_model=FinanceiroExtratosBancariosResponse, status_code=status.HTTP_201_CREATED)
async def criar_extrato(
    extrato: FinanceiroExtratosBancariosCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria um novo extrato bancário"""
    try:
        # Verificar se conta existe
        query = select(FinanceiroContas).where(FinanceiroContas.id_conta == extrato.id_conta)
        result = await db.execute(query)
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Conta não encontrada"
            )
        
        db_extrato = FinanceiroExtratosBancarios(**extrato.dict())
        db.add(db_extrato)
        await db.commit()
        await db.refresh(db_extrato)
        return db_extrato
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar extrato: {str(e)}"
        )

# ========== ORÇAMENTOS ==========

@router.get("/orcamentos")
async def listar_orcamentos(
    db: AsyncSession = Depends(get_db),
    ano: Optional[int] = Query(None),
    mes: Optional[int] = Query(None),
    conta_id: Optional[int] = Query(None),
    categoria: Optional[str] = Query(None),  # Novo filtro
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    # current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista todos os orçamentos - COM CATEGORIA E DESCRIÇÃO"""
    try:
        print("=== /orcamentos (com categoria e descrição) ===")
        
        from sqlalchemy import text
        
        # SQL com TODOS os campos incluindo categoria e descrição
        sql = """
        SELECT 
            id_orcamento,
            ano,
            mes,
            id_conta,
            valor_previsto,
            valor_realizado,
            categoria,
            descricao
        FROM fi.financeiro_orcamentos
        WHERE 1=1
        """
        
        params = {}
        
        if ano:
            sql += " AND ano = :ano"
            params['ano'] = ano
            
        if mes:
            sql += " AND mes = :mes"
            params['mes'] = mes
            
        if conta_id:
            sql += " AND id_conta = :conta_id"
            params['conta_id'] = conta_id
            
        if categoria:
            sql += " AND categoria ILIKE :categoria"
            params['categoria'] = f"%{categoria}%"
            
        sql += " ORDER BY ano DESC, mes DESC, categoria"
        sql += " LIMIT :limit OFFSET :skip"
        
        params['limit'] = limit
        params['skip'] = skip
        
        print(f"Executando SQL: {sql}")
        print(f"Parâmetros: {params}")
        
        result = await db.execute(text(sql), params)
        rows = result.fetchall()
        
        # Formatar resposta com TODOS os campos
        orcamentos = []
        for row in rows:
            orcamento = {
                "id_orcamento": row[0],
                "ano": row[1],
                "mes": row[2],
                "id_conta": row[3],
                "valor_previsto": float(row[4]) if row[4] else 0.0,
                "valor_realizado": float(row[5]) if row[5] else 0.0,
                "categoria": row[6] if row[6] is not None else "Não categorizado",
                "descricao": row[7] if row[7] is not None else f"Orçamento {row[1]}/{row[2]:02d}"
            }
            orcamentos.append(orcamento)
        
        print(f"Sucesso! Retornando {len(orcamentos)} orçamentos")
        return orcamentos
        
    except Exception as e:
        print(f"ERRO em /orcamentos: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

@router.post("/orcamentos")
async def criar_orcamento(
    orcamento_data: dict,
    db: AsyncSession = Depends(get_db),
    # current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria um novo orçamento - COM CATEGORIA E DESCRIÇÃO"""
    try:
        print("=== POST /orcamentos (com categoria e descrição) ===")
        print(f"Dados recebidos: {orcamento_data}")
        
        from sqlalchemy import text
        
        # SQL com TODOS os campos incluindo categoria e descrição
        sql = """
        INSERT INTO fi.financeiro_orcamentos 
        (ano, mes, id_conta, valor_previsto, valor_realizado, categoria, descricao)
        VALUES (:ano, :mes, :id_conta, :valor_previsto, :valor_realizado, :categoria, :descricao)
        RETURNING id_orcamento
        """
        
        params = {
            "ano": orcamento_data.get("ano"),
            "mes": orcamento_data.get("mes"),
            "id_conta": orcamento_data.get("id_conta"),
            "valor_previsto": float(orcamento_data.get("valor_previsto", 0)),
            "valor_realizado": 0.00,  # Inicialmente zero
            "categoria": orcamento_data.get("categoria", "Não categorizado"),
            "descricao": orcamento_data.get("descricao", "")
        }
        
        print(f"SQL de inserção: {sql}")
        print(f"Parâmetros: {params}")
        
        result = await db.execute(text(sql), params)
        await db.commit()
        
        novo_id = result.scalar()
        
        # Retornar o objeto criado
        return {
            "id_orcamento": novo_id,
            "ano": params["ano"],
            "mes": params["mes"],
            "id_conta": params["id_conta"],
            "valor_previsto": params["valor_previsto"],
            "valor_realizado": params["valor_realizado"],
            "categoria": params["categoria"],
            "descricao": params["descricao"]
        }
        
    except Exception as e:
        await db.rollback()
        print(f"ERRO ao criar orçamento: {str(e)}")
        import traceback
        traceback.print_exc()
        
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar orçamento: {str(e)}"
        )

@router.get("/orcamentos/{orcamento_id}")
async def get_orcamento(
    orcamento_id: int,
    db: AsyncSession = Depends(get_db),
    # current_user: UsuarioModel = Depends(get_current_user)
):
    """Obtém um orçamento específico - ESTRUTURA REAL"""
    try:
        print(f"=== GET /orcamentos/{orcamento_id} ===")
        
        from sqlalchemy import text
        
        sql = """
        SELECT 
            id_orcamento,
            ano,
            mes,
            id_conta,
            valor_previsto,
            valor_realizado
        FROM fi.financeiro_orcamentos
        WHERE id_orcamento = :id
        """
        
        result = await db.execute(text(sql), {"id": orcamento_id})
        row = result.fetchone()
        
        if not row:
            raise HTTPException(
                status_code=404,
                detail="Orçamento não encontrado"
            )
        
        # Formatar resposta
        orcamento = {
            "id_orcamento": row[0],
            "ano": row[1],
            "mes": row[2],
            "id_conta": row[3],
            "valor_previsto": float(row[4]) if row[4] else 0.0,
            "valor_realizado": float(row[5]) if row[5] else 0.0,
            "categoria": "",
            "descricao": f"Orçamento {row[1]}/{row[2]:02d}"
        }
        
        return orcamento
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERRO: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar orçamento: {str(e)}"
        )

@router.put("/orcamentos/{orcamento_id}/atualizar-campos")
async def atualizar_campos_orcamento(
    orcamento_id: int,
    db: AsyncSession = Depends(get_db),
    # current_user: UsuarioModel = Depends(get_current_user)
):
    """Atualiza registros antigos com valores padrão para categoria e descrição"""
    try:
        from sqlalchemy import text
        
        print(f"=== Atualizando campos para orçamento {orcamento_id} ===")
        
        # Primeiro, buscar o orçamento
        select_sql = """
        SELECT ano, mes, id_conta FROM fi.financeiro_orcamentos 
        WHERE id_orcamento = :id
        """
        
        result = await db.execute(text(select_sql), {"id": orcamento_id})
        orcamento = result.fetchone()
        
        if not orcamento:
            raise HTTPException(status_code=404, detail="Orçamento não encontrado")
        
        ano, mes, id_conta = orcamento
        
        # Atualizar com valores baseados nos dados existentes
        update_sql = """
        UPDATE fi.financeiro_orcamentos 
        SET 
            categoria = CASE 
                WHEN id_conta = 1 THEN 'Marketing'
                WHEN id_conta = 2 THEN 'TI'
                ELSE 'Geral'
            END,
            descricao = :descricao
        WHERE id_orcamento = :id
        """
        
        descricao = f"Orçamento {ano}/{mes:02d} - Conta {id_conta}"
        
        await db.execute(text(update_sql), {
            "id": orcamento_id,
            "descricao": descricao
        })
        await db.commit()
        
        return {
            "success": True,
            "message": f"Orçamento {orcamento_id} atualizado com categoria e descrição",
            "categoria": "Marketing" if id_conta == 1 else ("TI" if id_conta == 2 else "Geral"),
            "descricao": descricao
        }
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/orcamentos/atualizar-todos-campos")
async def atualizar_todos_campos(
    db: AsyncSession = Depends(get_db),
    # current_user: UsuarioModel = Depends(get_current_user)
):
    """Atualiza TODOS os registros antigos com categoria e descrição"""
    try:
        from sqlalchemy import text
        
        print("=== Atualizando TODOS os registros ===")
        
        # Contar registros sem categoria
        count_sql = "SELECT COUNT(*) FROM fi.financeiro_orcamentos WHERE categoria IS NULL OR descricao IS NULL"
        result = await db.execute(text(count_sql))
        total_para_atualizar = result.scalar()
        
        print(f"Total de registros para atualizar: {total_para_atualizar}")
        
        if total_para_atualizar == 0:
            return {"message": "Todos os registros já possuem categoria e descrição"}
        
        # Atualizar todos os registros
        update_sql = """
        UPDATE fi.financeiro_orcamentos 
        SET 
            categoria = COALESCE(categoria, 
                CASE 
                    WHEN id_conta = 1 THEN 'Marketing'
                    WHEN id_conta = 2 THEN 'TI'
                    WHEN id_conta = 3 THEN 'RH'
                    WHEN id_conta = 4 THEN 'Vendas'
                    ELSE 'Geral'
                END),
            descricao = COALESCE(descricao, 
                CONCAT('Orçamento ', ano, '/', LPAD(mes::text, 2, '0'), ' - Conta ', id_conta))
        WHERE categoria IS NULL OR descricao IS NULL
        """
        
        result = await db.execute(text(update_sql))
        await db.commit()
        
        linhas_afetadas = result.rowcount
        
        return {
            "success": True,
            "message": f"Atualizados {linhas_afetadas} registros com categoria e descrição",
            "total_atualizados": linhas_afetadas
        }
        
    except Exception as e:
        await db.rollback()
        print(f"ERRO: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/orcamentos/{orcamento_id}")
async def deletar_orcamento(
    orcamento_id: int,
    db: AsyncSession = Depends(get_db),
    # current_user: UsuarioModel = Depends(get_current_user)
):
    """Exclui um orçamento"""
    try:
        print(f"=== DELETE /orcamentos/{orcamento_id} ===")
        
        from sqlalchemy import text
        
        # Verificar se existe
        check_sql = "SELECT 1 FROM fi.financeiro_orcamentos WHERE id_orcamento = :id"
        check_result = await db.execute(text(check_sql), {"id": orcamento_id})
        if not check_result.fetchone():
            raise HTTPException(
                status_code=404,
                detail="Orçamento não encontrado"
            )
        
        # Excluir
        delete_sql = "DELETE FROM fi.financeiro_orcamentos WHERE id_orcamento = :id"
        await db.execute(text(delete_sql), {"id": orcamento_id})
        await db.commit()
        
        return {"message": "Orçamento excluído com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        print(f"ERRO: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao excluir orçamento: {str(e)}"
        )

@router.post("/orcamentos/inicializar-tabela")
async def inicializar_tabela_orcamentos(db: AsyncSession = Depends(get_db)):
    """Inicializa a tabela com dados de exemplo"""
    try:
        from sqlalchemy import text
        
        print("=== Inicializando tabela de orçamentos ===")
        
        # Verificar se já existem dados
        check_sql = "SELECT COUNT(*) FROM fi.financeiro_orcamentos"
        result = await db.execute(text(check_sql))
        count = result.scalar()
        
        if count > 0:
            return {
                "message": "Tabela já contém dados",
                "total_registros": count
            }
        
        # Dados de exemplo para 2024
        meses = [1, 2, 3]
        categorias_contas = [
            (1, 5000.00),  # Conta 1 - Marketing
            (1, 10000.00), # Conta 1 - TI
            (2, 30000.00), # Conta 2 - Salários
        ]
        
        registros_criados = 0
        for mes in meses:
            for idx, (conta_id, valor) in enumerate(categorias_contas):
                sql = """
                INSERT INTO fi.financeiro_orcamentos 
                (ano, mes, id_conta, valor_previsto, valor_realizado)
                VALUES (2024, :mes, :conta_id, :valor_previsto, :valor_realizado)
                """
                
                # Valor realizado = 80-90% do previsto
                valor_realizado = valor * (0.8 + (idx * 0.05))
                
                params = {
                    "mes": mes,
                    "conta_id": conta_id,
                    "valor_previsto": float(valor),
                    "valor_realizado": float(valor_realizado)
                }
                
                await db.execute(text(sql), params)
                registros_criados += 1
        
        await db.commit()
        
        return {
            "message": "Tabela inicializada com dados de exemplo",
            "registros_criados": registros_criados
        }
        
    except Exception as e:
        await db.rollback()
        print(f"ERRO: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao inicializar tabela: {str(e)}"
        )

@router.get("/orcamentos/dashboard")
async def dashboard_orcamentos(
    ano: int = Query(default=2024),
    db: AsyncSession = Depends(get_db)
):
    """Dashboard de orçamentos"""
    try:
        from sqlalchemy import text
        
        # Total por mês
        sql = """
        SELECT 
            mes,
            SUM(valor_previsto) as total_previsto,
            SUM(valor_realizado) as total_realizado
        FROM fi.financeiro_orcamentos
        WHERE ano = :ano
        GROUP BY mes
        ORDER BY mes
        """
        
        result = await db.execute(text(sql), {"ano": ano})
        rows = result.fetchall()
        
        # Totais gerais
        total_sql = """
        SELECT 
            SUM(valor_previsto) as total_previsto,
            SUM(valor_realizado) as total_realizado
        FROM fi.financeiro_orcamentos
        WHERE ano = :ano
        """
        
        total_result = await db.execute(text(total_sql), {"ano": ano})
        total_row = total_result.fetchone()
        
        data = []
        for row in rows:
            percentual = (row[2] / row[1] * 100) if row[1] > 0 else 0
            data.append({
                "mes": row[0],
                "total_previsto": float(row[1]),
                "total_realizado": float(row[2]),
                "percentual": round(float(percentual), 1)
            })
        
        return {
            "ano": ano,
            "total_geral": {
                "previsto": float(total_row[0]) if total_row[0] else 0.0,
                "realizado": float(total_row[1]) if total_row[1] else 0.0,
                "percentual": round((float(total_row[1]) / float(total_row[0]) * 100) if total_row[0] > 0 else 0, 1)
            },
            "por_mes": data
        }
        
    except Exception as e:
        print(f"ERRO no dashboard: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar dashboard: {str(e)}"
        )


# ========== FLUXO DE CAIXA ==========

@router.get("/fluxo-caixa", response_model=List[FinanceiroFluxoCaixaResponse])
async def listar_fluxo_caixa(
    db: AsyncSession = Depends(get_db),
    data_inicio: Optional[date] = Query(None),
    data_fim: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista o fluxo de caixa"""
    query = select(FinanceiroFluxoCaixa)
    
    if data_inicio:
        query = query.where(FinanceiroFluxoCaixa.data >= data_inicio)
    if data_fim:
        query = query.where(FinanceiroFluxoCaixa.data <= data_fim)
    
    query = query.offset(skip).limit(limit).order_by(desc(FinanceiroFluxoCaixa.data))
    
    result = await db.execute(query)
    fluxos = result.scalars().all()
    return fluxos

@router.post("/fluxo-caixa/gerar")
async def gerar_fluxo_caixa(
    data_inicio: date,
    data_fim: date,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Gera fluxo de caixa para um período"""
    try:
        # Buscar lançamentos no período
        query = select(FinanceiroLancamentos).where(
            and_(
                FinanceiroLancamentos.data_lancamento >= data_inicio,
                FinanceiroLancamentos.data_lancamento <= data_fim
            )
        ).order_by(FinanceiroLancamentos.data_lancamento)
        
        result = await db.execute(query)
        lancamentos = result.scalars().all()
        
        # Calcular fluxo por dia
        fluxo_por_dia = {}
        for lancamento in lancamentos:
            data = lancamento.data_lancamento
            if data not in fluxo_por_dia:
                fluxo_por_dia[data] = {
                    'entradas': Decimal('0.00'),
                    'saidas': Decimal('0.00')
                }
            
            if lancamento.tipo == 'receita':
                fluxo_por_dia[data]['entradas'] += lancamento.valor
            else:
                fluxo_por_dia[data]['saidas'] += lancamento.valor
        
        # Gerar registro de fluxo
        fluxos_gerados = []
        data_atual = data_inicio
        saldo_anterior = Decimal('0.00')
        
        while data_atual <= data_fim:
            entradas = fluxo_por_dia.get(data_atual, {}).get('entradas', Decimal('0.00'))
            saidas = fluxo_por_dia.get(data_atual, {}).get('saidas', Decimal('0.00'))
            saldo_final = saldo_anterior + entradas - saidas
            
            # Verificar se já existe fluxo para esta data
            query = select(FinanceiroFluxoCaixa).where(FinanceiroFluxoCaixa.data == data_atual)
            result = await db.execute(query)
            fluxo_existente = result.scalar_one_or_none()
            
            if fluxo_existente:
                # Atualizar fluxo existente
                fluxo_existente.saldo_inicial = saldo_anterior
                fluxo_existente.entradas = entradas
                fluxo_existente.saidas = saidas
                fluxo_existente.saldo_final = saldo_final
                fluxos_gerados.append(fluxo_existente)
            else:
                # Criar novo fluxo
                fluxo = FinanceiroFluxoCaixa(
                    data=data_atual,
                    saldo_inicial=saldo_anterior,
                    entradas=entradas,
                    saidas=saidas,
                    saldo_final=saldo_final
                )
                db.add(fluxo)
                fluxos_gerados.append(fluxo)
            
            saldo_anterior = saldo_final
            data_atual += timedelta(days=1)
        
        await db.commit()
        
        return {
            "message": f"Fluxo de caixa gerado para o período {data_inicio} a {data_fim}",
            "periodo": {
                "inicio": data_inicio.isoformat(),
                "fim": data_fim.isoformat()
            },
            "total_dias": len(fluxos_gerados),
            "fluxos_gerados": [
                {
                    "data": fluxo.data.isoformat(),
                    "entradas": float(fluxo.entradas),
                    "saidas": float(fluxo.saidas),
                    "saldo_final": float(fluxo.saldo_final)
                }
                for fluxo in fluxos_gerados
            ]
        }
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar fluxo de caixa: {str(e)}"
        )

# ========== PLANO DE CONTAS ==========

@router.get("/plano-contas", response_model=List[ContabilidadePlanoContasResponse])
async def listar_plano_contas(
    db: AsyncSession = Depends(get_db),
    tipo: Optional[str] = Query(None),
    nivel: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista todas as contas do plano de contas"""
    query = select(ContabilidadePlanoContas)
    
    if tipo:
        query = query.where(ContabilidadePlanoContas.tipo == tipo)
    if nivel:
        query = query.where(ContabilidadePlanoContas.nivel == nivel)
    
    query = query.offset(skip).limit(limit).order_by(ContabilidadePlanoContas.codigo)
    
    result = await db.execute(query)
    contas = result.scalars().all()
    return contas

@router.post("/plano-contas", response_model=ContabilidadePlanoContasResponse, status_code=status.HTTP_201_CREATED)
async def criar_conta_plano(
    conta: ContabilidadePlanoContasCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria uma nova conta no plano de contas"""
    try:
        # Verificar se código já existe
        query = select(ContabilidadePlanoContas).where(ContabilidadePlanoContas.codigo == conta.codigo)
        result = await db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código de conta já existe"
            )
        
        db_conta = ContabilidadePlanoContas(**conta.dict())
        db.add(db_conta)
        await db.commit()
        await db.refresh(db_conta)
        return db_conta
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar conta no plano: {str(e)}"
        )

# ========== NOTAS FISCAIS ==========

@router.get("/notas-fiscais", response_model=List[FiscalNotasFiscaisResponse])
async def listar_notas_fiscais(
    db: AsyncSession = Depends(get_db),
    tipo: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    data_inicio: Optional[date] = Query(None),
    data_fim: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista todas as notas fiscais"""
    query = select(FiscalNotasFiscais)
    
    if tipo:
        query = query.where(FiscalNotasFiscais.tipo == tipo)
    if status:
        query = query.where(FiscalNotasFiscais.status == status)
    if data_inicio:
        query = query.where(FiscalNotasFiscais.data_emissao >= data_inicio)
    if data_fim:
        query = query.where(FiscalNotasFiscais.data_emissao <= data_fim)
    
    query = query.offset(skip).limit(limit).order_by(desc(FiscalNotasFiscais.data_emissao))
    
    result = await db.execute(query)
    notas = result.scalars().all()
    return notas

@router.post("/notas-fiscais", response_model=FiscalNotasFiscaisResponse, status_code=status.HTTP_201_CREATED)
async def criar_nota_fiscal(
    nota: FiscalNotasFiscaisCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria uma nova nota fiscal"""
    try:
        # Verificar se número de nota já existe
        query = select(FiscalNotasFiscais).where(FiscalNotasFiscais.numero_nota == nota.numero_nota)
        result = await db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Número de nota fiscal já existe"
            )
        
        db_nota = FiscalNotasFiscais(**nota.dict())
        db.add(db_nota)
        await db.commit()
        await db.refresh(db_nota)
        return db_nota
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar nota fiscal: {str(e)}"
        )

# ========== IMPOSTOS ==========

@router.post("/impostos", response_model=FiscalImpostosResponse, status_code=status.HTTP_201_CREATED)
async def criar_imposto(
    imposto: FiscalImpostosCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria um novo imposto"""
    try:
        # Verificar se nota fiscal existe
        query = select(FiscalNotasFiscais).where(FiscalNotasFiscais.id_nota == imposto.id_nota)
        result = await db.execute(query)
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nota fiscal não encontrada"
            )
        
        db_imposto = FiscalImpostos(**imposto.dict())
        db.add(db_imposto)
        await db.commit()
        await db.refresh(db_imposto)
        return db_imposto
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar imposto: {str(e)}"
        )

# ========== RELATÓRIOS ==========

@router.get("/relatorios/receitas-despesas")
async def relatorio_receitas_despesas(
    data_inicio: date,
    data_fim: date,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Relatório de receitas e despesas por período"""
    try:
        # Receitas por categoria (simplificado)
        receitas_query = select(
            func.sum(FinanceiroLancamentos.valor).label("total")
        ).where(
            and_(
                FinanceiroLancamentos.tipo == 'receita',
                FinanceiroLancamentos.data_lancamento >= data_inicio,
                FinanceiroLancamentos.data_lancamento <= data_fim
            )
        )
        receitas_result = await db.execute(receitas_query)
        total_receitas = receitas_result.scalar() or Decimal('0.00')
        
        # Despesas por categoria (simplificado)
        despesas_query = select(
            func.sum(FinanceiroLancamentos.valor).label("total")
        ).where(
            and_(
                FinanceiroLancamentos.tipo == 'despesa',
                FinanceiroLancamentos.data_lancamento >= data_inicio,
                FinanceiroLancamentos.data_lancamento <= data_fim
            )
        )
        despesas_result = await db.execute(despesas_query)
        total_despesas = despesas_result.scalar() or Decimal('0.00')
        
        # Lançamentos detalhados
        lancamentos_query = select(FinanceiroLancamentos).where(
            and_(
                FinanceiroLancamentos.data_lancamento >= data_inicio,
                FinanceiroLancamentos.data_lancamento <= data_fim
            )
        ).order_by(FinanceiroLancamentos.data_lancamento)
        
        lancamentos_result = await db.execute(lancamentos_query)
        lancamentos = lancamentos_result.scalars().all()
        
        return {
            "periodo": {
                "inicio": data_inicio.isoformat(),
                "fim": data_fim.isoformat()
            },
            "resumo": {
                "total_receitas": float(total_receitas),
                "total_despesas": float(total_despesas),
                "saldo_periodo": float(total_receitas - total_despesas)
            },
            "lancamentos": [
                {
                    "id": l.id_lancamento,
                    "data": l.data_lancamento.isoformat(),
                    "descricao": l.descricao,
                    "tipo": l.tipo,
                    "valor": float(l.valor),
                    "conta_id": l.id_conta
                }
                for l in lancamentos
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar relatório: {str(e)}"
        )
    
@router.get("/dashboard/data")
async def get_dashboard_data(
    db: AsyncSession = Depends(get_db),
    # current_user: UsuarioModel = Depends(get_current_user)
):
    """Obtém dados reais do banco para o dashboard"""
    try:
        print("=== GET /fi/dashboard/data ===")
        
        from sqlalchemy import text
        from datetime import datetime, timedelta
        
        # 1. ESTATÍSTICAS BÁSICAS
        estatisticas = {}
        
        # Total de contas
        query_contas = "SELECT COUNT(*) FROM fi.financeiro_contas WHERE ativo = true"
        result = await db.execute(text(query_contas))
        estatisticas['contas_ativas'] = result.scalar() or 0
        
        query_total_contas = "SELECT COUNT(*) FROM fi.financeiro_contas"
        result = await db.execute(text(query_total_contas))
        estatisticas['total_contas'] = result.scalar() or 0
        
        # Total de lançamentos
        query_lancamentos = "SELECT COUNT(*) FROM fi.financeiro_lancamentos"
        result = await db.execute(text(query_lancamentos))
        estatisticas['total_lancamentos'] = result.scalar() or 0
        
        # 2. RECEITAS E DESPESAS DO MÊS ATUAL
        mes_atual = datetime.now().month
        ano_atual = datetime.now().year
        
        # Receitas do mês
        query_receitas = """
        SELECT COALESCE(SUM(valor), 0) 
        FROM fi.financeiro_lancamentos 
        WHERE tipo = 'receita' 
        AND EXTRACT(MONTH FROM data_lancamento) = :mes
        AND EXTRACT(YEAR FROM data_lancamento) = :ano
        """
        result = await db.execute(text(query_receitas), {"mes": mes_atual, "ano": ano_atual})
        estatisticas['receitas_mes'] = float(result.scalar() or 0)
        
        # Despesas do mês
        query_despesas = """
        SELECT COALESCE(SUM(valor), 0) 
        FROM fi.financeiro_lancamentos 
        WHERE tipo = 'despesa' 
        AND EXTRACT(MONTH FROM data_lancamento) = :mes
        AND EXTRACT(YEAR FROM data_lancamento) = :ano
        """
        result = await db.execute(text(query_despesas), {"mes": mes_atual, "ano": ano_atual})
        estatisticas['despesas_mes'] = float(result.scalar() or 0)
        
        # Resultado do mês
        estatisticas['resultado_mes'] = estatisticas['receitas_mes'] - estatisticas['despesas_mes']
        
        # 3. SALDO TOTAL (soma dos saldos iniciais das contas)
        query_saldo = "SELECT COALESCE(SUM(saldo_inicial), 0) FROM fi.financeiro_contas WHERE ativo = true"
        result = await db.execute(text(query_saldo))
        estatisticas['saldo_total'] = float(result.scalar() or 0)
        
        # 4. ÚLTIMOS LANÇAMENTOS (últimos 10)
        query_ultimos_lancamentos = """
        SELECT 
            id_lancamento,
            descricao,
            tipo,
            valor,
            data_lancamento,
            created_at
        FROM fi.financeiro_lancamentos 
        ORDER BY data_lancamento DESC, created_at DESC 
        LIMIT 10
        """
        
        result = await db.execute(text(query_ultimos_lancamentos))
        rows = result.fetchall()
        
        ultimos_lancamentos = []
        for row in rows:
            lancamento = {
                "id": row[0],
                "descricao": row[1],
                "tipo": row[2],
                "valor": float(row[3]) if row[3] else 0,
                "data": row[4].isoformat() if row[4] else None,
                "created_at": row[5].isoformat() if row[5] else None
            }
            ultimos_lancamentos.append(lancamento)
        
        # 5. DADOS PARA GRÁFICO (últimos 6 meses)
        seis_meses_atras = datetime.now() - timedelta(days=180)
        
        query_dados_grafico = """
        SELECT 
            EXTRACT(MONTH FROM data_lancamento) as mes,
            EXTRACT(YEAR FROM data_lancamento) as ano,
            tipo,
            SUM(valor) as total
        FROM fi.financeiro_lancamentos 
        WHERE data_lancamento >= :data_inicio
        GROUP BY EXTRACT(YEAR FROM data_lancamento), EXTRACT(MONTH FROM data_lancamento), tipo
        ORDER BY ano, mes
        """
        
        result = await db.execute(text(query_dados_grafico), {"data_inicio": seis_meses_atras})
        rows_grafico = result.fetchall()
        
        # Organizar dados para gráfico
        dados_grafico = {
            "receitas": [],
            "despesas": [],
            "meses": []
        }
        
        meses_unicos = set()
        for row in rows_grafico:
            mes_num = int(row[0])
            ano_num = int(row[1])
            tipo = row[2]
            total = float(row[3]) if row[3] else 0
            
            # Formatar mês/ano para exibição
            mes_formatado = f"{mes_num:02d}/{str(ano_num)[-2:]}"
            meses_unicos.add(mes_formatado)
            
            if tipo == 'receita':
                dados_grafico["receitas"].append({
                    "mes": mes_formatado,
                    "valor": total
                })
            elif tipo == 'despesa':
                dados_grafico["despesas"].append({
                    "mes": mes_formatado,
                    "valor": total
                })
        
        dados_grafico["meses"] = sorted(list(meses_unicos))
        
        # 6. TOP CATEGORIAS DE ORÇAMENTOS
        query_top_categorias = """
        SELECT 
            categoria,
            SUM(valor_previsto) as total_previsto,
            SUM(valor_realizado) as total_realizado
        FROM fi.financeiro_orcamentos
        WHERE categoria IS NOT NULL AND categoria != ''
        GROUP BY categoria
        ORDER BY total_previsto DESC
        LIMIT 5
        """
        
        result = await db.execute(text(query_top_categorias))
        rows_categorias = result.fetchall()
        
        top_categorias = []
        for row in rows_categorias:
            categoria = {
                "nome": row[0],
                "previsto": float(row[1]) if row[1] else 0,
                "realizado": float(row[2]) if row[2] else 0,
                "percentual": round((float(row[2]) / float(row[1]) * 100) if row[1] > 0 else 0, 1)
            }
            top_categorias.append(categoria)
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "estatisticas": estatisticas,
            "ultimos_lancamentos": ultimos_lancamentos,
            "dados_grafico": dados_grafico,
            "top_categorias": top_categorias,
            "endpoints": {
                "contas": "/api/fi/contas",
                "lancamentos": "/api/fi/lancamentos",
                "orcamentos": "/api/fi/orcamentos",
                "fluxo_caixa": "/api/fi/fluxo-caixa",
                "notas_fiscais": "/api/fi/notas-fiscais"
            }
        }
        
    except Exception as e:
        print(f"ERRO em /dashboard/data: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            "status": "error",
            "message": str(e),
            "estatisticas": {
                "total_contas": 0,
                "contas_ativas": 0,
                "total_lancamentos": 0,
                "receitas_mes": 0,
                "despesas_mes": 0,
                "saldo_total": 0,
                "resultado_mes": 0
            },
            "ultimos_lancamentos": [],
            "dados_grafico": {
                "receitas": [],
                "despesas": [],
                "meses": []
            },
            "top_categorias": []
        }

# ========== HEALTH CHECK ==========

@router.get("/health")
async def health_check_financeiro():
    """Verifica se o módulo Financeiro está funcionando"""
    return {
        "status": "healthy",
        "module": "Financeiro",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/api/fi/contas",
            "/api/fi/lancamentos",
            "/api/fi/orcamentos",
            "/api/fi/fluxo-caixa",
            "/api/fi/notas-fiscais",
            "/api/fi/dashboard"
        ]
    }

@router.get("/dashboard")
async def dashboard_financeiro(
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Dashboard do módulo Financeiro"""
    try:
        # Total de contas
        contas_query = select(func.count()).select_from(FinanceiroContas)
        contas_result = await db.execute(contas_query)
        total_contas = contas_result.scalar() or 0
        
        # Contas ativas
        contas_ativas_query = select(func.count()).select_from(FinanceiroContas).where(FinanceiroContas.ativo == True)
        contas_ativas_result = await db.execute(contas_ativas_query)
        contas_ativas = contas_ativas_result.scalar() or 0
        
        # Total de lançamentos
        lancamentos_query = select(func.count()).select_from(FinanceiroLancamentos)
        lancamentos_result = await db.execute(lancamentos_query)
        total_lancamentos = lancamentos_result.scalar() or 0
        
        # Receitas do mês
        mes_atual = datetime.now().month
        ano_atual = datetime.now().year
        
        receitas_query = select(func.coalesce(func.sum(FinanceiroLancamentos.valor), 0))\
    .select_from(FinanceiroLancamentos)\
    .where(
        and_(
            FinanceiroLancamentos.tipo == 'receita',
            func.extract('month', FinanceiroLancamentos.data_lancamento) == mes_atual,
            func.extract('year', FinanceiroLancamentos.data_lancamento) == ano_atual
        )
    )
        receitas_result = await db.execute(receitas_query)
        receitas_mes = receitas_result.scalar() or Decimal('0.00')
        
        # Despesas do mês
        despesas_query = select(func.coalesce(func.sum(FinanceiroLancamentos.valor), 0))\
    .select_from(FinanceiroLancamentos)\
    .where(
        and_(
            FinanceiroLancamentos.tipo == 'despesa',
            func.extract('month', FinanceiroLancamentos.data_lancamento) == mes_atual,
            func.extract('year', FinanceiroLancamentos.data_lancamento) == ano_atual
        )
    )
        despesas_result = await db.execute(despesas_query)
        despesas_mes = despesas_result.scalar() or Decimal('0.00')
        
        # Saldo total (soma dos saldos iniciais das contas)
        saldo_query = select(func.coalesce(func.sum(FinanceiroContas.saldo_inicial), 0))\
    .select_from(FinanceiroContas)
        saldo_result = await db.execute(saldo_query)
        saldo_total = saldo_result.scalar() or Decimal('0.00')
        
        # Últimos lançamentos
        ultimos_lancamentos_query = select(FinanceiroLancamentos).order_by(
            desc(FinanceiroLancamentos.data_lancamento)
        ).limit(10)
        ultimos_lancamentos_result = await db.execute(ultimos_lancamentos_query)
        ultimos_lancamentos = ultimos_lancamentos_result.scalars().all()

        return {
            "status": "ativo",
            "modulo": "Financeiro (FI)",
            "estatisticas": {
                "total_contas": total_contas,
                "contas_ativas": contas_ativas,
                "total_lancamentos": total_lancamentos,
                "receitas_mes": float(receitas_mes),
                "despesas_mes": float(despesas_mes),
                "saldo_total": float(saldo_total),
                "resultado_mes": float(receitas_mes - despesas_mes)
            },
            "ultimos_lancamentos": [
                {
                    "id": lancamento.id_lancamento,
                    "descricao": lancamento.descricao,
                    "tipo": lancamento.tipo,
                    "valor": float(lancamento.valor),
                    "data": lancamento.data_lancamento.isoformat() if lancamento.data_lancamento else None
                }
                for lancamento in ultimos_lancamentos
            ],
            "endpoints": {
                "contas": "/api/fi/contas",
                "lancamentos": "/api/fi/lancamentos",
                "orcamentos": "/api/fi/orcamentos",
                "fluxo_caixa": "/api/fi/fluxo-caixa",
                "notas_fiscais": "/api/fi/notas-fiscais"
            }
        }
    except Exception as e:
        import traceback
        print(f"Erro no dashboard financeiro: {str(e)}")
        print(traceback.format_exc())
        return {
            "status": "error",
            "message": f"Erro ao gerar dashboard: {str(e)}",
            "estatisticas": {
                "total_contas": 0,
                "contas_ativas": 0,
                "total_lancamentos": 0,
                "receitas_mes": 0,
                "despesas_mes": 0,
                "saldo_total": 0,
                "resultado_mes": 0
            },
            "ultimos_lancamentos": []
        }

@router.get("/debug-contas")
async def debug_contas_detalhado(db: AsyncSession = Depends(get_db)):
    """Debug completo da rota contas"""
    import traceback
    from sqlalchemy import text, inspect
    
    debug_info = {
        "status": "iniciando",
        "steps": [],
        "errors": []
    }
    
    try:
        # PASSO 1: Verificar conexão com banco
        debug_info["steps"].append("1. Testando conexão com banco...")
        result = await db.execute(text("SELECT 1 as test, CURRENT_TIMESTAMP as agora"))
        row = result.fetchone()
        debug_info["database_test"] = {
            "connected": True,
            "test_value": row[0],
            "timestamp": str(row[1])
        }
        
        # PASSO 2: Verificar tabela
        debug_info["steps"].append("2. Verificando tabela financeiro_contas...")
        result = await db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'fi' 
                AND table_name = 'financeiro_contas'
            )
        """))
        table_exists = result.scalar()
        debug_info["table_exists"] = table_exists
        
        if table_exists:
            # PASSO 3: Verificar estrutura da tabela
            debug_info["steps"].append("3. Verificando estrutura da tabela...")
            result = await db.execute(text("""
                SELECT 
                    column_name, 
                    data_type,
                    is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'fi' 
                AND table_name = 'financeiro_contas'
                ORDER BY ordinal_position
            """))
            columns = result.fetchall()
            debug_info["table_columns"] = [
                {"name": col[0], "type": col[1], "nullable": col[2]}
                for col in columns
            ]
            
            # PASSO 4: Contar registros
            debug_info["steps"].append("4. Contando registros...")
            result = await db.execute(text("SELECT COUNT(*) FROM fi.financeiro_contas"))
            count = result.scalar()
            debug_info["row_count"] = count
            
            # PASSO 5: Buscar alguns registros
            if count > 0:
                debug_info["steps"].append("5. Buscando alguns registros...")
                result = await db.execute(text("SELECT * FROM fi.financeiro_contas LIMIT 3"))
                rows = result.fetchall()
                debug_info["sample_data"] = []
                for row in rows:
                    debug_info["sample_data"].append({
                        "id_conta": row[0],
                        "nome": row[1],
                        "tipo": row[2],
                        "saldo_inicial": float(row[3]) if row[3] else 0,
                        "data_abertura": row[4].isoformat() if row[4] else None,
                        "ativo": row[5]
                    })
        
        # PASSO 6: Testar SQLAlchemy
        debug_info["steps"].append("6. Testando SQLAlchemy ORM...")
        try:
            # Verificar modelo
            inspector = inspect(FinanceiroContas)
            debug_info["sqlalchemy_model"] = {
                "table_name": FinanceiroContas.__tablename__,
                "schema": FinanceiroContas.__table_args__.get('schema') if hasattr(FinanceiroContas, '__table_args__') else None,
                "columns": [c.key for c in inspector.columns]
            }
            
            # Tentar fazer query
            query = select(FinanceiroContas).limit(2)
            debug_info["sqlalchemy_query"] = str(query)
            
            result = await db.execute(query)
            contas = result.scalars().all()
            debug_info["sqlalchemy_results_count"] = len(contas)
            
            if contas:
                debug_info["sqlalchemy_sample"] = [
                    {
                        "id": c.id_conta,
                        "nome": c.nome,
                        "tipo": c.tipo
                    }
                    for c in contas
                ]
                
        except Exception as e:
            debug_info["sqlalchemy_error"] = str(e)
            debug_info["sqlalchemy_traceback"] = traceback.format_exc()
        
        debug_info["status"] = "success"
        
    except Exception as e:
        debug_info["status"] = "error"
        debug_info["error"] = str(e)
        debug_info["traceback"] = traceback.format_exc()
    
    return debug_info   

