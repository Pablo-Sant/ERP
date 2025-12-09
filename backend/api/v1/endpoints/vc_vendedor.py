from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.deps import get_session
from schemas.vc_vendedor_schema import VendedorCreate, VendedorUpdate, VendedorResponse
from services.vendedor_service import VendedorService

router = APIRouter()

@router.post("/", response_model=VendedorResponse, status_code=status.HTTP_201_CREATED)
async def criar_vendedor(
    vendedor: VendedorCreate,
    db: AsyncSession = Depends(get_session)
):
    try:
        return await VendedorService.criar(vendedor, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[VendedorResponse])
async def listar_vendedores(db: AsyncSession = Depends(get_session)):
    try:
        return await VendedorService.get_all(db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{vendedor_id}", response_model=VendedorResponse)
async def buscar_vendedor_por_id(
    vendedor_id: int,
    db: AsyncSession = Depends(get_session)
):
    try:
        return await VendedorService.get_by_id(vendedor_id, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/buscar/nome", response_model=List[VendedorResponse])
async def buscar_vendedor_por_nome(
    nome: str = Query(..., min_length=2, description="Nome ou parte do nome"),
    db: AsyncSession = Depends(get_session)
):
    try:
        return await VendedorService.buscar_por_nome(nome, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/buscar/documento", response_model=VendedorResponse)
async def buscar_vendedor_por_cpf_cnpj(
    cpf_cnpj: str = Query(..., min_length=11, description="CPF ou CNPJ"),
    db: AsyncSession = Depends(get_session)
):
    try:
        return await VendedorService.buscar_por_cpf_cnpj(cpf_cnpj, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{vendedor_id}", response_model=VendedorResponse)
async def atualizar_vendedor(
    vendedor_id: int,
    vendedor_update: VendedorUpdate,
    db: AsyncSession = Depends(get_session)
):
    try:
        return await VendedorService.update(vendedor_id, vendedor_update, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "não encontrado" in str(e).lower() 
            else status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{vendedor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_vendedor(
    vendedor_id: int,
    db: AsyncSession = Depends(get_session)
):
    try:
        sucesso = await VendedorService.delete(vendedor_id, db)
        if not sucesso:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendedor não encontrado")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))