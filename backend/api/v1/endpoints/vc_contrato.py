from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import date
from core.deps import get_session
from schemas.vc_contrato_schema import ContratoCreate, ContratoUpdate, ContratoResponse
from services.vc_contrato_service import ContratoService

router = APIRouter()

@router.post("/", response_model=ContratoResponse, status_code=status.HTTP_201_CREATED)
async def criar_contrato(
    contrato: ContratoCreate,
    db: AsyncSession = Depends(get_session)
):
    try:
        return await ContratoService.criar(contrato, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[ContratoResponse])
async def listar_contratos(
    db: AsyncSession = Depends(get_session)
):
    try:
        return await ContratoService.get_all(db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{contrato_id}", response_model=ContratoResponse)
async def buscar_contrato_por_id(
    contrato_id: int,
    db: AsyncSession = Depends(get_session)
):
    try:
        return await ContratoService.get_by_id(contrato_id, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/cliente/{cliente_finalid}", response_model=List[ContratoResponse])
async def buscar_contratos_por_cliente(
    cliente_finalid: int,
    db: AsyncSession = Depends(get_session)
):
    try:
        return await ContratoService.buscar_por_cliente(cliente_finalid, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/vendedor/{vendedorid}", response_model=List[ContratoResponse])
async def buscar_contratos_por_vendedor(
    vendedorid: int,
    db: AsyncSession = Depends(get_session)
):
    try:
        return await ContratoService.buscar_por_vendedor(vendedorid, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/vencimento/em", response_model=List[ContratoResponse])
async def buscar_contratos_vencendo_em(
    data_vencimento: date = Query(..., description="Data de vencimento (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_session)
):
    try:
        return await ContratoService.buscar_vencendo_em(data_vencimento, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/vencimento/proximos", response_model=List[ContratoResponse])
async def buscar_contratos_a_vencer(
    dias: int = Query(30, ge=1, le=365, description="Número de dias para buscar"),
    db: AsyncSession = Depends(get_session)
):
    try:
        return await ContratoService.buscar_a_vencer(db, dias)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{contrato_id}", response_model=ContratoResponse)
async def atualizar_contrato(
    contrato_id: int,
    contrato_update: ContratoUpdate,
    db: AsyncSession = Depends(get_session)
):
    try:
        return await ContratoService.update(contrato_id, contrato_update, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "não encontrado" in str(e).lower() 
            else status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/{contrato_id}/renovar", response_model=ContratoResponse)
async def renovar_contrato(
    contrato_id: int,
    nova_data_vencimento: date = Query(..., description="Nova data de vencimento (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_session)
):
    try:
        return await ContratoService.renovar_contrato(contrato_id, nova_data_vencimento, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{contrato_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_contrato(
    contrato_id: int,
    db: AsyncSession = Depends(get_session)
):
    try:
        sucesso = await ContratoService.delete(contrato_id, db)
        if not sucesso:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contrato não encontrado")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))