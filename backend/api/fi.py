# api/fi_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc
from typing import List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal

from core.deps import get_session
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

@router.get("/contas", response_model=List[FinanceiroContasResponse])
async def listar_contas(
    db: AsyncSession = Depends(get_session),
    tipo: Optional[str] = Query(None),
    ativo: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista todas as contas financeiras"""
    query = select(FinanceiroContas)
    
    if tipo:
        query = query.where(FinanceiroContas.tipo == tipo)
    if ativo is not None:
        query = query.where(FinanceiroContas.ativo == ativo)
    
    query = query.offset(skip).limit(limit).order_by(FinanceiroContas.nome)
    
    result = await db.execute(query)
    contas = result.scalars().all()
    return contas

@router.get("/contas/{conta_id}", response_model=FinanceiroContasResponse)
async def get_conta(
    conta_id: int,
    db: AsyncSession = Depends(get_session),
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
    db: AsyncSession = Depends(get_session),
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
    db: AsyncSession = Depends(get_session),
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
    db: AsyncSession = Depends(get_session),
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
    db: AsyncSession = Depends(get_session),
    conta_id: Optional[int] = Query(None),
    tipo: Optional[str] = Query(None),
    data_inicio: Optional[date] = Query(None),
    data_fim: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista todos os lançamentos financeiros"""
    query = select(FinanceiroLancamentos)
    
    if conta_id:
        query = query.where(FinanceiroLancamentos.id_conta == conta_id)
    if tipo:
        query = query.where(FinanceiroLancamentos.tipo == tipo)
    if data_inicio:
        query = query.where(FinanceiroLancamentos.data_lancamento >= data_inicio)
    if data_fim:
        query = query.where(FinanceiroLancamentos.data_lancamento <= data_fim)
    
    query = query.offset(skip).limit(limit).order_by(desc(FinanceiroLancamentos.data_lancamento))
    
    result = await db.execute(query)
    lancamentos = result.scalars().all()
    return lancamentos

@router.get("/lancamentos/{lancamento_id}", response_model=FinanceiroLancamentosResponse)
async def get_lancamento(
    lancamento_id: int,
    db: AsyncSession = Depends(get_session),
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
    db: AsyncSession = Depends(get_session),
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
    db: AsyncSession = Depends(get_session),
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
    db: AsyncSession = Depends(get_session),
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
    db: AsyncSession = Depends(get_session),
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
    db: AsyncSession = Depends(get_session),
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

@router.get("/orcamentos", response_model=List[FinanceiroOrcamentosResponse])
async def listar_orcamentos(
    db: AsyncSession = Depends(get_session),
    ano: Optional[int] = Query(None),
    mes: Optional[int] = Query(None),
    conta_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista todos os orçamentos"""
    query = select(FinanceiroOrcamentos)
    
    if ano:
        query = query.where(FinanceiroOrcamentos.ano == ano)
    if mes:
        query = query.where(FinanceiroOrcamentos.mes == mes)
    if conta_id:
        query = query.where(FinanceiroOrcamentos.id_conta == conta_id)
    
    query = query.offset(skip).limit(limit).order_by(
        desc(FinanceiroOrcamentos.ano), desc(FinanceiroOrcamentos.mes)
    )
    
    result = await db.execute(query)
    orcamentos = result.scalars().all()
    return orcamentos

@router.post("/orcamentos", response_model=FinanceiroOrcamentosResponse, status_code=status.HTTP_201_CREATED)
async def criar_orcamento(
    orcamento: FinanceiroOrcamentosCreate,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria um novo orçamento"""
    try:
        # Verificar se conta existe
        query = select(FinanceiroContas).where(FinanceiroContas.id_conta == orcamento.id_conta)
        result = await db.execute(query)
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Conta não encontrada"
            )
        
        # Verificar se já existe orçamento para este período e conta
        query = select(FinanceiroOrcamentos).where(
            and_(
                FinanceiroOrcamentos.ano == orcamento.ano,
                FinanceiroOrcamentos.mes == orcamento.mes,
                FinanceiroOrcamentos.id_conta == orcamento.id_conta
            )
        )
        result = await db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe orçamento para este período e conta"
            )
        
        db_orcamento = FinanceiroOrcamentos(**orcamento.dict())
        db.add(db_orcamento)
        await db.commit()
        await db.refresh(db_orcamento)
        return db_orcamento
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar orçamento: {str(e)}"
        )

# ========== FLUXO DE CAIXA ==========

@router.get("/fluxo-caixa", response_model=List[FinanceiroFluxoCaixaResponse])
async def listar_fluxo_caixa(
    db: AsyncSession = Depends(get_session),
    data_inicio: Optional[date] = Query(None),
    data_fim: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UsuarioModel = Depends(get_current_user)
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
    db: AsyncSession = Depends(get_session),
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
    db: AsyncSession = Depends(get_session),
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
    db: AsyncSession = Depends(get_session),
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
    db: AsyncSession = Depends(get_session),
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
    db: AsyncSession = Depends(get_session),
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
    db: AsyncSession = Depends(get_session),
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

# ========== DASHBOARD FINANCEIRO ==========

@router.get("/dashboard")
async def dashboard_financeiro(
    db: AsyncSession = Depends(get_session),
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
        
        receitas_query = select(func.coalesce(func.sum(FinanceiroLancamentos.valor), 0)).where(
            and_(
                FinanceiroLancamentos.tipo == 'receita',
                func.extract('month', FinanceiroLancamentos.data_lancamento) == mes_atual,
                func.extract('year', FinanceiroLancamentos.data_lancamento) == ano_atual
            )
        )
        receitas_result = await db.execute(receitas_query)
        receitas_mes = receitas_result.scalar() or Decimal('0.00')
        
        # Despesas do mês
        despesas_query = select(func.coalesce(func.sum(FinanceiroLancamentos.valor), 0)).where(
            and_(
                FinanceiroLancamentos.tipo == 'despesa',
                func.extract('month', FinanceiroLancamentos.data_lancamento) == mes_atual,
                func.extract('year', FinanceiroLancamentos.data_lancamento) == ano_atual
            )
        )
        despesas_result = await db.execute(despesas_query)
        despesas_mes = despesas_result.scalar() or Decimal('0.00')
        
        # Saldo total
        saldo_query = select(func.coalesce(func.sum(FinanceiroContas.saldo_inicial), 0))
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
                    "id": l.id_lancamento,
                    "descricao": l.descricao,
                    "tipo": l.tipo,
                    "valor": float(l.valor),
                    "data": l.data_lancamento.isoformat() if l.data_lancamento else None
                }
                for l in ultimos_lancamentos
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar dashboard: {str(e)}"
        )

# ========== RELATÓRIOS ==========

@router.get("/relatorios/receitas-despesas")
async def relatorio_receitas_despesas(
    data_inicio: date,
    data_fim: date,
    db: AsyncSession = Depends(get_session),
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