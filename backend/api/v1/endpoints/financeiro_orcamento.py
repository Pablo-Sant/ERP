from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from schemas.financeiro_orcamentos import FinanceiroOrcamentosCreate, FinanceiroOrcamentosResponse
from services.financeiro_orcamento_service import FinanceiroOrcamentosService


router = APIRouter()


@router.get('/', response_model=List[FinanceiroOrcamentosResponse])
async def get_planos_conta(db: AsyncSession = Depends(get_session)):
    return await FinanceiroOrcamentosService.get_all(db)


@router.post('/', response_model=FinanceiroOrcamentosResponse, status_code=201)
async def post_plano_conta(payload: FinanceiroOrcamentosCreate, db: AsyncSession = Depends(get_session)):
    return await FinanceiroOrcamentosService.create(payload, db)


@router.get('/{id}', response_model=FinanceiroOrcamentosResponse)
async def get_plano_conta(id: int, db: AsyncSession = Depends(get_session)):
    return await FinanceiroOrcamentosService.get_by_id(id, db)


@router.put('/{id}', response_model=FinanceiroOrcamentosResponse)
async def put_plano_conta(id: int, payload: FinanceiroOrcamentosCreate, db: AsyncSession = Depends(get_session)):
    return await FinanceiroOrcamentosService.update(id, payload, db)


@router.delete('/{id}', status_code=204)
async def delete_plano_conta(id: int, db: AsyncSession = Depends(get_session)):
    return await FinanceiroOrcamentosService.delete(id, db)
