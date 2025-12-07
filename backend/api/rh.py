# api/rh_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, func
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime, date

from core.deps import get_session
from models.rh_colaboradores_model import Colaborador
from models.rh_funcoes_model import Funcao
from models.rh_folha_pagamento_model import FolhaPagamento
from models.rh_recrutamento_model import Recrutamento
from models.rh_avaliacao_desempenho_model import AvaliacaoDesempenho
from models.rh_beneficios_model import Beneficio
from models.rh_colaborador_beneficio_model import ColaboradorBeneficio
from schemas.rh_colaborador_schema import (
    ColaboradorCreate, ColaboradorUpdate, ColaboradorResponse
)
from schemas.rh_funcoes_schema import (
    FuncaoCreate, FuncaoUpdate, FuncaoResponse
)
from schemas.rh_folha_pagamento_schema import (
    FolhaPagamentoCreate, FolhaPagamentoUpdate, FolhaPagamentoResponse
)
from schemas.rh_recrutamento_schema import (
    RecrutamentoCreate, RecrutamentoUpdate, RecrutamentoResponse
)
from schemas.rh_avaliacao_desempenho_schema import (
    AvaliacaoDesempenhoCreate, AvaliacaoDesempenhoUpdate, AvaliacaoDesempenhoResponse
)
from schemas.rh_beneficios_schema import (
    BeneficioCreate, BeneficioUpdate, BeneficioResponse
)
from schemas.rh_colaborador_beneficio_schema import (
    ColaboradorBeneficioCreate, ColaboradorBeneficioResponse
)
from api.auth import get_current_user
from models.usuario import UsuarioModel

router = APIRouter(prefix="/rh", tags=["Recursos Humanos"])

# ========== COLABORADORES ==========

@router.get("/colaboradores", response_model=List[ColaboradorResponse])
async def listar_colaboradores(
    db: AsyncSession = Depends(get_session),
    funcao_id: Optional[int] = Query(None),
    ativo: Optional[int] = Query(None, ge=0, le=1),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista todos os colaboradores com filtros"""
    query = select(Colaborador).options(
        selectinload(Colaborador.funcao_rel),
        selectinload(Colaborador.beneficios).selectinload(ColaboradorBeneficio.beneficio)
    )
    
    # Aplicar filtros
    filters = []
    
    if funcao_id:
        filters.append(Colaborador.funcao_id == funcao_id)
    if ativo is not None:
        filters.append(Colaborador.ativo == ativo)
    if search:
        filters.append(
            or_(
                Colaborador.nome.ilike(f"%{search}%"),
                Colaborador.cpf.ilike(f"%{search}%"),
                Colaborador.email.ilike(f"%{search}%") if Colaborador.email else False
            )
        )
    
    if filters:
        query = query.where(and_(*filters))
    
    query = query.offset(skip).limit(limit).order_by(Colaborador.nome)
    
    result = await db.execute(query)
    colaboradores = result.scalars().all()
    return colaboradores

@router.get("/colaboradores/{colaborador_id}", response_model=ColaboradorResponse)
async def get_colaborador(
    colaborador_id: int,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Obtém um colaborador específico com seus relacionamentos"""
    query = select(Colaborador).where(Colaborador.id == colaborador_id).options(
        selectinload(Colaborador.funcao_rel),
        selectinload(Colaborador.beneficios).selectinload(ColaboradorBeneficio.beneficio),
        selectinload(Colaborador.folhas_pagamento),
        selectinload(Colaborador.recrutamentos),
        selectinload(Colaborador.avaliacoes)
    )
    
    result = await db.execute(query)
    colaborador = result.scalar_one_or_none()
    
    if not colaborador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não encontrado"
        )
    
    return colaborador

@router.post("/colaboradores", response_model=ColaboradorResponse, status_code=status.HTTP_201_CREATED)
async def criar_colaborador(
    colaborador: ColaboradorCreate,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria um novo colaborador"""
    try:
        # Verificar se CPF já existe
        query = select(Colaborador).where(Colaborador.cpf == colaborador.cpf)
        result = await db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF já cadastrado"
            )
        
        # Verificar se função existe
        if colaborador.funcao_id:
            funcao_query = select(Funcao).where(Funcao.id == colaborador.funcao_id)
            funcao_result = await db.execute(funcao_query)
            if not funcao_result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Função não encontrada"
                )
        
        # Validar datas
        if colaborador.data_de_recrutamento > colaborador.data_contratacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data de recrutamento não pode ser posterior à data de contratação"
            )
        
        db_colaborador = Colaborador(**colaborador.dict())
        db.add(db_colaborador)
        await db.commit()
        await db.refresh(db_colaborador)
        return db_colaborador
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar colaborador: {str(e)}"
        )

@router.put("/colaboradores/{colaborador_id}", response_model=ColaboradorResponse)
async def atualizar_colaborador(
    colaborador_id: int,
    colaborador_update: ColaboradorUpdate,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Atualiza um colaborador existente"""
    query = select(Colaborador).where(Colaborador.id == colaborador_id)
    result = await db.execute(query)
    db_colaborador = result.scalar_one_or_none()
    
    if not db_colaborador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não encontrado"
        )
    
    update_data = colaborador_update.dict(exclude_unset=True)
    
    # Verificar duplicidade de CPF se for atualizado
    if 'cpf' in update_data:
        query = select(Colaborador).where(
            Colaborador.cpf == update_data['cpf'],
            Colaborador.id != colaborador_id
        )
        result = await db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF já cadastrado para outro colaborador"
            )
    
    # Verificar se função existe se for atualizar
    if 'funcao_id' in update_data and update_data['funcao_id']:
        funcao_query = select(Funcao).where(Funcao.id == update_data['funcao_id'])
        funcao_result = await db.execute(funcao_query)
        if not funcao_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Função não encontrada"
            )
    
    for field, value in update_data.items():
        setattr(db_colaborador, field, value)
    
    try:
        await db.commit()
        await db.refresh(db_colaborador)
        return db_colaborador
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar colaborador: {str(e)}"
        )

@router.delete("/colaboradores/{colaborador_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_colaborador(
    colaborador_id: int,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Remove um colaborador (soft delete - marca como inativo)"""
    query = select(Colaborador).where(Colaborador.id == colaborador_id)
    result = await db.execute(query)
    colaborador = result.scalar_one_or_none()
    
    if not colaborador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não encontrado"
        )
    
    try:
        # Soft delete - marca como inativo
        colaborador.ativo = 0
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover colaborador: {str(e)}"
        )

# ========== FUNÇÕES ==========

@router.get("/funcoes", response_model=List[FuncaoResponse])
async def listar_funcoes(
    db: AsyncSession = Depends(get_session),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista todas as funções"""
    query = select(Funcao)
    
    if search:
        query = query.where(
            or_(
                Funcao.nome.ilike(f"%{search}%"),
                Funcao.descricao.ilike(f"%{search}%") if Funcao.descricao else False
            )
        )
    
    query = query.offset(skip).limit(limit).order_by(Funcao.nome)
    result = await db.execute(query)
    funcoes = result.scalars().all()
    return funcoes

@router.get("/funcoes/{funcao_id}", response_model=FuncaoResponse)
async def get_funcao(
    funcao_id: int,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Obtém uma função específica"""
    query = select(Funcao).where(Funcao.id == funcao_id)
    result = await db.execute(query)
    funcao = result.scalar_one_or_none()
    
    if not funcao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Função não encontrada"
        )
    
    return funcao

@router.post("/funcoes", response_model=FuncaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_funcao(
    funcao: FuncaoCreate,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria uma nova função"""
    try:
        db_funcao = Funcao(**funcao.dict())
        db.add(db_funcao)
        await db.commit()
        await db.refresh(db_funcao)
        return db_funcao
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar função: {str(e)}"
        )

@router.put("/funcoes/{funcao_id}", response_model=FuncaoResponse)
async def atualizar_funcao(
    funcao_id: int,
    funcao_update: FuncaoUpdate,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Atualiza uma função existente"""
    query = select(Funcao).where(Funcao.id == funcao_id)
    result = await db.execute(query)
    db_funcao = result.scalar_one_or_none()
    
    if not db_funcao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Função não encontrada"
        )
    
    update_data = funcao_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_funcao, field, value)
    
    try:
        await db.commit()
        await db.refresh(db_funcao)
        return db_funcao
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar função: {str(e)}"
        )

@router.delete("/funcoes/{funcao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_funcao(
    funcao_id: int,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Exclui uma função"""
    query = select(Funcao).where(Funcao.id == funcao_id)
    result = await db.execute(query)
    funcao = result.scalar_one_or_none()
    
    if not funcao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Função não encontrada"
        )
    
    # Verificar se há colaboradores associados
    colaboradores_query = select(Colaborador).where(Colaborador.funcao_id == funcao_id)
    colaboradores_result = await db.execute(colaboradores_query)
    if colaboradores_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível excluir função com colaboradores associados"
        )
    
    try:
        await db.delete(funcao)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir função: {str(e)}"
        )

# ========== FOLHA DE PAGAMENTO ==========

@router.get("/folha-pagamento", response_model=List[FolhaPagamentoResponse])
async def listar_folhas_pagamento(
    db: AsyncSession = Depends(get_session),
    colaborador_id: Optional[int] = Query(None),
    mes: Optional[int] = Query(None, ge=1, le=12),
    ano: Optional[int] = Query(None, ge=2000, le=2100),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista folhas de pagamento com filtros"""
    query = select(FolhaPagamento)
    
    filters = []
    if colaborador_id:
        filters.append(FolhaPagamento.colaborador_id == colaborador_id)
    if mes:
        filters.append(FolhaPagamento.mes == mes)
    if ano:
        filters.append(FolhaPagamento.ano == ano)
    
    if filters:
        query = query.where(and_(*filters))
    
    query = query.offset(skip).limit(limit).order_by(FolhaPagamento.ano.desc(), FolhaPagamento.mes.desc())
    
    result = await db.execute(query)
    folhas = result.scalars().all()
    return folhas

@router.get("/folha-pagamento/{folha_id}", response_model=FolhaPagamentoResponse)
async def get_folha_pagamento(
    folha_id: int,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Obtém uma folha de pagamento específica"""
    query = select(FolhaPagamento).where(FolhaPagamento.id == folha_id)
    result = await db.execute(query)
    folha = result.scalar_one_or_none()
    
    if not folha:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folha de pagamento não encontrada"
        )
    
    return folha

@router.post("/folha-pagamento", response_model=FolhaPagamentoResponse, status_code=status.HTTP_201_CREATED)
async def criar_folha_pagamento(
    folha: FolhaPagamentoCreate,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria uma nova folha de pagamento"""
    try:
        # Verificar se colaborador existe
        colaborador_query = select(Colaborador).where(Colaborador.id == folha.colaborador_id)
        colaborador_result = await db.execute(colaborador_query)
        if not colaborador_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Colaborador não encontrado"
            )
        
        # Verificar se já existe folha para o mesmo mês/ano/colaborador
        existente_query = select(FolhaPagamento).where(
            FolhaPagamento.colaborador_id == folha.colaborador_id,
            FolhaPagamento.mes == folha.mes,
            FolhaPagamento.ano == folha.ano
        )
        existente_result = await db.execute(existente_query)
        if existente_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe folha de pagamento para este colaborador no mês/ano informado"
            )
        
        # Validar valores
        if folha.descontos and folha.descontos > folha.salario_base:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Descontos não podem ser maiores que o salário base"
            )
        
        if folha.salario_liquido > folha.salario_base:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Salário líquido não pode ser maior que o salário base"
            )
        
        db_folha = FolhaPagamento(**folha.dict())
        db.add(db_folha)
        await db.commit()
        await db.refresh(db_folha)
        return db_folha
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar folha de pagamento: {str(e)}"
        )

@router.put("/folha-pagamento/{folha_id}", response_model=FolhaPagamentoResponse)
async def atualizar_folha_pagamento(
    folha_id: int,
    folha_update: FolhaPagamentoUpdate,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Atualiza uma folha de pagamento existente"""
    query = select(FolhaPagamento).where(FolhaPagamento.id == folha_id)
    result = await db.execute(query)
    db_folha = result.scalar_one_or_none()
    
    if not db_folha:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folha de pagamento não encontrada"
        )
    
    update_data = folha_update.dict(exclude_unset=True)
    
    # Validar valores se estiverem sendo atualizados
    if 'descontos' in update_data and update_data['descontos']:
        if update_data['descontos'] > db_folha.salario_base:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Descontos não podem ser maiores que o salário base"
            )
    
    if 'salario_liquido' in update_data:
        if update_data['salario_liquido'] > db_folha.salario_base:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Salário líquido não pode ser maior que o salário base"
            )
    
    for field, value in update_data.items():
        setattr(db_folha, field, value)
    
    try:
        await db.commit()
        await db.refresh(db_folha)
        return db_folha
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar folha de pagamento: {str(e)}"
        )

# ========== RECRUTAMENTO ==========

@router.get("/recrutamentos", response_model=List[RecrutamentoResponse])
async def listar_recrutamentos(
    db: AsyncSession = Depends(get_session),
    colaborador_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    data_inicio: Optional[date] = Query(None),
    data_fim: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista recrutamentos com filtros"""
    query = select(Recrutamento)
    
    filters = []
    if colaborador_id:
        filters.append(Recrutamento.colaborador_id == colaborador_id)
    if status:
        filters.append(Recrutamento.status.ilike(f"%{status}%"))
    if data_inicio:
        filters.append(Recrutamento.data_recrutamento >= data_inicio)
    if data_fim:
        filters.append(Recrutamento.data_recrutamento <= data_fim)
    
    if filters:
        query = query.where(and_(*filters))
    
    query = query.offset(skip).limit(limit).order_by(Recrutamento.data_recrutamento.desc())
    
    result = await db.execute(query)
    recrutamentos = result.scalars().all()
    return recrutamentos

@router.post("/recrutamentos", response_model=RecrutamentoResponse, status_code=status.HTTP_201_CREATED)
async def criar_recrutamento(
    recrutamento: RecrutamentoCreate,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria um novo registro de recrutamento"""
    try:
        # Verificar se colaborador existe
        colaborador_query = select(Colaborador).where(Colaborador.id == recrutamento.colaborador_id)
        colaborador_result = await db.execute(colaborador_query)
        if not colaborador_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Colaborador não encontrado"
            )
        
        db_recrutamento = Recrutamento(**recrutamento.dict())
        db.add(db_recrutamento)
        await db.commit()
        await db.refresh(db_recrutamento)
        return db_recrutamento
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar recrutamento: {str(e)}"
        )

# ========== AVALIAÇÃO DE DESEMPENHO ==========

@router.get("/avaliacoes", response_model=List[AvaliacaoDesempenhoResponse])
async def listar_avaliacoes(
    db: AsyncSession = Depends(get_session),
    colaborador_id: Optional[int] = Query(None),
    nota_minima: Optional[int] = Query(None, ge=0, le=10),
    data_inicio: Optional[date] = Query(None),
    data_fim: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista avaliações de desempenho com filtros"""
    query = select(AvaliacaoDesempenho)
    
    filters = []
    if colaborador_id:
        filters.append(AvaliacaoDesempenho.colaborador_id == colaborador_id)
    if nota_minima is not None:
        filters.append(AvaliacaoDesempenho.nota >= nota_minima)
    if data_inicio:
        filters.append(AvaliacaoDesempenho.data_avaliacao >= data_inicio)
    if data_fim:
        filters.append(AvaliacaoDesempenho.data_avaliacao <= data_fim)
    
    if filters:
        query = query.where(and_(*filters))
    
    query = query.offset(skip).limit(limit).order_by(AvaliacaoDesempenho.data_avaliacao.desc())
    
    result = await db.execute(query)
    avaliacoes = result.scalars().all()
    return avaliacoes

@router.post("/avaliacoes", response_model=AvaliacaoDesempenhoResponse, status_code=status.HTTP_201_CREATED)
async def criar_avaliacao(
    avaliacao: AvaliacaoDesempenhoCreate,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria uma nova avaliação de desempenho"""
    try:
        # Verificar se colaborador existe
        colaborador_query = select(Colaborador).where(Colaborador.id == avaliacao.colaborador_id)
        colaborador_result = await db.execute(colaborador_query)
        if not colaborador_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Colaborador não encontrado"
            )
        
        # Validar nota
        if avaliacao.nota < 0 or avaliacao.nota > 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nota deve estar entre 0 e 10"
            )
        
        db_avaliacao = AvaliacaoDesempenho(**avaliacao.dict())
        db.add(db_avaliacao)
        await db.commit()
        await db.refresh(db_avaliacao)
        return db_avaliacao
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar avaliação: {str(e)}"
        )

# ========== BENEFÍCIOS ==========

@router.get("/beneficios", response_model=List[BeneficioResponse])
async def listar_beneficios(
    db: AsyncSession = Depends(get_session),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista todos os benefícios"""
    query = select(Beneficio)
    
    if search:
        query = query.where(
            or_(
                Beneficio.nome.ilike(f"%{search}%"),
                Beneficio.descricao.ilike(f"%{search}%") if Beneficio.descricao else False
            )
        )
    
    query = query.offset(skip).limit(limit).order_by(Beneficio.nome)
    result = await db.execute(query)
    beneficios = result.scalars().all()
    return beneficios

@router.post("/beneficios", response_model=BeneficioResponse, status_code=status.HTTP_201_CREATED)
async def criar_beneficio(
    beneficio: BeneficioCreate,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria um novo benefício"""
    try:
        db_beneficio = Beneficio(**beneficio.dict())
        db.add(db_beneficio)
        await db.commit()
        await db.refresh(db_beneficio)
        return db_beneficio
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar benefício: {str(e)}"
        )

# ========== ASSOCIAÇÃO COLABORADOR-BENEFÍCIO ==========

@router.get("/colaboradores/{colaborador_id}/beneficios", response_model=List[BeneficioResponse])
async def listar_beneficios_colaborador(
    colaborador_id: int,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista todos os benefícios de um colaborador"""
    # Verificar se colaborador existe
    colaborador_query = select(Colaborador).where(Colaborador.id == colaborador_id)
    colaborador_result = await db.execute(colaborador_query)
    if not colaborador_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colaborador não encontrado"
        )
    
    # Buscar associações e benefícios
    query = select(Beneficio).join(
        ColaboradorBeneficio, Beneficio.id == ColaboradorBeneficio.beneficio_id
    ).where(ColaboradorBeneficio.colaborador_id == colaborador_id)
    
    result = await db.execute(query)
    beneficios = result.scalars().all()
    return beneficios

@router.post("/colaboradores/{colaborador_id}/beneficios", response_model=ColaboradorBeneficioResponse, status_code=status.HTTP_201_CREATED)
async def adicionar_beneficio_colaborador(
    colaborador_id: int,
    beneficio_colaborador: ColaboradorBeneficioCreate,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Associa um benefício a um colaborador"""
    if beneficio_colaborador.colaborador_id != colaborador_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID do colaborador na URL não corresponde ao ID no corpo da requisição"
        )
    
    try:
        # Verificar se colaborador existe
        colaborador_query = select(Colaborador).where(Colaborador.id == colaborador_id)
        colaborador_result = await db.execute(colaborador_query)
        if not colaborador_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Colaborador não encontrado"
            )
        
        # Verificar se benefício existe
        beneficio_query = select(Beneficio).where(Beneficio.id == beneficio_colaborador.beneficio_id)
        beneficio_result = await db.execute(beneficio_query)
        if not beneficio_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Benefício não encontrado"
            )
        
        # Verificar se já existe associação
        associacao_query = select(ColaboradorBeneficio).where(
            ColaboradorBeneficio.colaborador_id == colaborador_id,
            ColaboradorBeneficio.beneficio_id == beneficio_colaborador.beneficio_id
        )
        associacao_result = await db.execute(associacao_query)
        if associacao_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Benefício já associado ao colaborador"
            )
        
        db_associacao = ColaboradorBeneficio(**beneficio_colaborador.dict())
        db.add(db_associacao)
        await db.commit()
        await db.refresh(db_associacao)
        return db_associacao
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao associar benefício: {str(e)}"
        )

@router.delete("/colaboradores/{colaborador_id}/beneficios/{beneficio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_beneficio_colaborador(
    colaborador_id: int,
    beneficio_id: int,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Remove a associação de um benefício com um colaborador"""
    query = select(ColaboradorBeneficio).where(
        ColaboradorBeneficio.colaborador_id == colaborador_id,
        ColaboradorBeneficio.beneficio_id == beneficio_id
    )
    result = await db.execute(query)
    associacao = result.scalar_one_or_none()
    
    if not associacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associação não encontrada"
        )
    
    try:
        await db.delete(associacao)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover associação: {str(e)}"
        )

# ========== DASHBOARD RH ==========

@router.get("/dashboard")
async def rh_dashboard(
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Dashboard do módulo de Recursos Humanos"""
    try:
        # Total de colaboradores
        total_colaboradores_query = select(func.count()).select_from(Colaborador)
        total_colaboradores_result = await db.execute(total_colaboradores_query)
        total_colaboradores = total_colaboradores_result.scalar() or 0
        
        # Colaboradores ativos (usando campo ativo)
        ativos_query = select(func.count()).select_from(Colaborador).where(Colaborador.ativo == 1)
        ativos_result = await db.execute(ativos_query)
        ativos = ativos_result.scalar() or 0
        
        # Colaboradores inativos
        inativos = total_colaboradores - ativos
        
        # Total de funções
        total_funcoes_query = select(func.count()).select_from(Funcao)
        total_funcoes_result = await db.execute(total_funcoes_query)
        total_funcoes = total_funcoes_result.scalar() or 0
        
        # Total de folhas de pagamento
        total_folhas_query = select(func.count()).select_from(FolhaPagamento)
        total_folhas_result = await db.execute(total_folhas_query)
        total_folhas = total_folhas_result.scalar() or 0
        
        # Total de benefícios
        total_beneficios_query = select(func.count()).select_from(Beneficio)
        total_beneficios_result = await db.execute(total_beneficios_query)
        total_beneficios = total_beneficios_result.scalar() or 0
        
        # Total de avaliações
        total_avaliacoes_query = select(func.count()).select_from(AvaliacaoDesempenho)
        total_avaliacoes_result = await db.execute(total_avaliacoes_query)
        total_avaliacoes = total_avaliacoes_result.scalar() or 0
        
        # Média de avaliações
        media_avaliacoes_query = select(func.avg(AvaliacaoDesempenho.nota))
        media_avaliacoes_result = await db.execute(media_avaliacoes_query)
        media_avaliacoes = media_avaliacoes_result.scalar() or 0
        
        # Últimos colaboradores contratados - COM selectinload
        ultimos_contratados_query = select(Colaborador).options(
            selectinload(Colaborador.funcao_rel)
        ).order_by(
            Colaborador.data_contratacao.desc()
        ).limit(5)
        
        ultimos_contratados_result = await db.execute(ultimos_contratados_query)
        ultimos_contratados = ultimos_contratados_result.scalars().all()
        
        # Colaboradores por função - Query correta
        colaboradores_por_funcao_query = select(
            Funcao.nome,
            func.count(Colaborador.id).label('quantidade')
        ).outerjoin(
            Colaborador, Colaborador.funcao_id == Funcao.id
        ).where(
            Colaborador.ativo == 1
        ).group_by(Funcao.id, Funcao.nome)
        
        colaboradores_por_funcao_result = await db.execute(colaboradores_por_funcao_query)
        colaboradores_por_funcao = [
            {"funcao": row[0] or "Sem função", "quantidade": row[1]}
            for row in colaboradores_por_funcao_result.all()
        ]
        
        # Folha de pagamento do último mês
        ultimo_mes = datetime.now().month
        ultimo_ano = datetime.now().year
        
        folha_ultimo_mes_query = select(func.sum(FolhaPagamento.salario_liquido)).where(
            FolhaPagamento.mes == ultimo_mes,
            FolhaPagamento.ano == ultimo_ano
        )
        folha_ultimo_mes_result = await db.execute(folha_ultimo_mes_query)
        total_folha_ultimo_mes = folha_ultimo_mes_result.scalar() or 0
        
        return {
            "status": "ativo",
            "modulo": "Recursos Humanos (RH)",
            "estatisticas": {
                "total_colaboradores": total_colaboradores,
                "colaboradores_ativos": ativos,
                "colaboradores_inativos": inativos,
                "total_funcoes": total_funcoes,
                "total_folhas_pagamento": total_folhas,
                "total_beneficios": total_beneficios,
                "total_avaliacoes": total_avaliacoes,
                "media_avaliacoes": round(float(media_avaliacoes), 2),
                "folha_pagamento_ultimo_mes": float(total_folha_ultimo_mes)
            },
            "distribuicao_funcoes": colaboradores_por_funcao,
            "ultimas_contratacoes": [
                {
                    "id": c.id,
                    "nome": c.nome,
                    "funcao": c.funcao_rel.nome if c.funcao_rel else "Sem função",
                    "data_contratacao": c.data_contratacao.isoformat() if c.data_contratacao else None,
                    "salario": float(c.salario) if c.salario else 0
                }
                for c in ultimos_contratados
            ],
            "endpoints": {
                "colaboradores": "/api/rh/colaboradores",
                "funcoes": "/api/rh/funcoes",
                "folha_pagamento": "/api/rh/folha-pagamento",
                "recrutamentos": "/api/rh/recrutamentos",
                "avaliacoes": "/api/rh/avaliacoes",
                "beneficios": "/api/rh/beneficios"
            }
        }
    except Exception as e:
        # Log detalhado do erro
        print(f"ERROR in rh_dashboard: {str(e)}")
        import traceback
        traceback.print_exc()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar dashboard: {str(e)}"
        )

# ========== RELATÓRIOS ==========

@router.get("/relatorios/folha-pagamento/{ano}/{mes}")
async def relatorio_folha_pagamento_mensal(
    ano: int,
    mes: int,
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Relatório consolidado da folha de pagamento de um mês específico"""
    try:
        # Buscar todas as folhas do mês
        folhas_query = select(FolhaPagamento).where(
            FolhaPagamento.ano == ano,
            FolhaPagamento.mes == mes
        )
        folhas_result = await db.execute(folhas_query)
        folhas = folhas_result.scalars().all()
        
        if not folhas:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma folha de pagamento encontrada para o mês/ano informado"
            )
        
        total_salario_base = sum(f.salario_base for f in folhas)
        total_descontos = sum(f.descontos or 0 for f in folhas)
        total_salario_liquido = sum(f.salario_liquido for f in folhas)
        
        # Buscar colaboradores com folha
        colaboradores_ids = [f.colaborador_id for f in folhas]
        colaboradores_query = select(Colaborador).where(Colaborador.id.in_(colaboradores_ids))
        colaboradores_result = await db.execute(colaboradores_query)
        colaboradores = {c.id: c for c in colaboradores_result.scalars().all()}
        
        detalhes = []
        for folha in folhas:
            colaborador = colaboradores.get(folha.colaborador_id)
            if colaborador:
                detalhes.append({
                    "colaborador_id": folha.colaborador_id,
                    "colaborador_nome": colaborador.nome,
                    "salario_base": float(folha.salario_base),
                    "descontos": float(folha.descontos or 0),
                    "salario_liquido": float(folha.salario_liquido),
                    "funcao": colaborador.funcao_rel.nome if colaborador.funcao_rel else "Sem função"
                })
        
        return {
            "ano": ano,
            "mes": mes,
            "total_funcionarios": len(folhas),
            "total_salario_base": float(total_salario_base),
            "total_descontos": float(total_descontos),
            "total_salario_liquido": float(total_salario_liquido),
            "media_salario_liquido": float(total_salario_liquido / len(folhas)) if folhas else 0,
            "detalhes": detalhes
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar relatório: {str(e)}"
        )

@router.get("/relatorios/colaboradores-por-funcao")
async def relatorio_colaboradores_por_funcao(
    db: AsyncSession = Depends(get_session),
    #current_user: UsuarioModel = Depends(get_current_user)
):
    """Relatório: Distribuição de colaboradores por função"""
    try:
        query = select(
            Funcao.nome,
            func.count(Colaborador.id).label('quantidade'),
            func.avg(Colaborador.salario).label('media_salario')
        ).outerjoin(
            Colaborador, Colaborador.funcao_id == Funcao.id
        ).where(
            Colaborador.ativo == 1
        ).group_by(Funcao.id, Funcao.nome)
        
        result = await db.execute(query)
        dados = result.all()
        
        relatorio = [
            {
                "funcao": row[0] or "Sem função",
                "quantidade": row[1],
                "media_salario": float(row[2] or 0)
            }
            for row in dados
        ]
        
        return {
            "total_colaboradores": sum(item["quantidade"] for item in relatorio),
            "distribuicao": relatorio
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar relatório: {str(e)}"
        )

# ========== HEALTH CHECK ==========

@router.get("/health")
async def health_check():
    """Verifica se o módulo RH está funcionando"""
    return {
        "status": "healthy",
        "module": "Recursos Humanos",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/api/rh/colaboradores",
            "/api/rh/funcoes",
            "/api/rh/folha-pagamento",
            "/api/rh/recrutamentos",
            "/api/rh/avaliacoes",
            "/api/rh/beneficios",
            "/api/rh/dashboard"
        ]
    }