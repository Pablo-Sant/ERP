
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from core.deps import get_session
from schemas.vc_cliente_final_schema import (
    ClienteFinalCreate, 
    ClienteFinalUpdate, 
    ClienteFinalResponse
)
from services.cliente_final_service import ClienteFinalService

router = APIRouter()

@router.post("/", 
    response_model=ClienteFinalResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo cliente final",
    description="Cria um novo cliente final no sistema"
)
async def criar_cliente_final(
    cliente: ClienteFinalCreate,
    db: AsyncSession = Depends(get_session)
):
    """Cria um novo cliente final"""
    try:
        novo_cliente = await ClienteFinalService.criar(cliente, db)
        return novo_cliente
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", 
    response_model=List[ClienteFinalResponse],
    summary="Listar todos os clientes finais",
    description="Retorna todos os clientes finais cadastrados"
)
async def listar_clientes_finais(
    db: AsyncSession = Depends(get_session)
):
    """Lista todos os clientes finais"""
    clientes = await ClienteFinalService.get_all(db)
    return clientes

@router.get("/{cliente_id}", 
    response_model=ClienteFinalResponse,
    summary="Buscar cliente por ID",
    description="Busca um cliente final pelo seu ID"
)
async def buscar_cliente_final(
    cliente_id: int,
    db: AsyncSession = Depends(get_session)
):
    """Busca cliente final por ID"""
    cliente = await ClienteFinalService.get_by_id(cliente_id, db)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    return cliente

@router.get("/buscar/nome/{nome}", 
    response_model=List[ClienteFinalResponse],
    summary="Buscar clientes por nome",
    description="Busca clientes finais por nome (busca parcial)"
)
async def buscar_cliente_por_nome(
    nome: str,
    db: AsyncSession = Depends(get_session)
):
    """Busca clientes por nome"""
    clientes = await ClienteFinalService.buscar_por_nome(nome, db)
    return clientes

@router.get("/buscar/documento/{cpf_cnpj}", 
    response_model=Optional[ClienteFinalResponse],
    summary="Buscar cliente por CPF/CNPJ",
    description="Busca cliente final pelo CPF ou CNPJ"
)
async def buscar_cliente_por_documento(
    cpf_cnpj: str,
    db: AsyncSession = Depends(get_session)
):
    """Busca cliente por CPF/CNPJ"""
    cliente = await ClienteFinalService.buscar_por_cpf_cnpj(cpf_cnpj, db)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com CPF/CNPJ {cpf_cnpj} não encontrado"
        )
    return cliente

@router.put("/{cliente_id}", 
    response_model=ClienteFinalResponse,
    summary="Atualizar cliente final",
    description="Atualiza os dados de um cliente final existente"
)
async def atualizar_cliente_final(
    cliente_id: int,
    cliente_update: ClienteFinalUpdate,
    db: AsyncSession = Depends(get_session)
):
    """Atualiza cliente final"""
    try:
        cliente_atualizado = await ClienteFinalService.update(
            cliente_id, cliente_update, db
        )
        if not cliente_atualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente com ID {cliente_id} não encontrado"
            )
        return cliente_atualizado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{cliente_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir cliente final",
    description="Remove um cliente final do sistema"
)
async def excluir_cliente_final(
    cliente_id: int,
    db: AsyncSession = Depends(get_session)
):
    """Exclui cliente final"""
    try:
        sucesso = await ClienteFinalService.delete(cliente_id, db)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente com ID {cliente_id} não encontrado"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )