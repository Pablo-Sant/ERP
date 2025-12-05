from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from services.financeiro_extrato_service import FinanceiroExtratoService

from schemas.financeiro_extratos_bancarios import (
    FinanceiroExtratosBancariosCreate,
    FinanceiroExtratosBancariosUpdate,
    FinanceiroExtratosBancariosResponse
)

router = APIRouter()



@router.get('/', response_model=List[FinanceiroExtratosBancariosResponse])
async def listar_extratos(db: AsyncSession = Depends(get_session)):
    return await FinanceiroExtratoService.listar(db)



@router.post('/', response_model=FinanceiroExtratosBancariosResponse, status_code=status.HTTP_201_CREATED)
async def criar_extrato(payload: FinanceiroExtratosBancariosCreate, db: AsyncSession = Depends(get_session)):
    return await FinanceiroExtratoService.criar(payload, db)



@router.get('/{id_extrato}', response_model=FinanceiroExtratosBancariosResponse)
async def obter_extrato(id_extrato: int, db: AsyncSession = Depends(get_session)):
    return await FinanceiroExtratoService.obter_por_id(id_extrato, db)



@router.put('/{id_extrato}', response_model=FinanceiroExtratosBancariosResponse)
async def atualizar_extrato(id_extrato: int, payload: FinanceiroExtratosBancariosUpdate, db: AsyncSession = Depends(get_session)):
    return await FinanceiroExtratoService.atualizar(id_extrato, payload, db)



@router.delete('/{id_extrato}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_extrato(id_extrato: int, db: AsyncSession = Depends(get_session)):
    await FinanceiroExtratoService.deletar(id_extrato, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
