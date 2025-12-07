from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.financeiro_fluxo_caixa import FinanceiroFluxoCaixa
from schemas.financeiro_fluxo_caixa import FinanceiroFluxoCaixaCreate, FinanceiroFluxoCaixaResponse
from services.financeiro_fluxo_caixa_service import FinanceiroFluxoCaixaService

router = APIRouter()



@router.get('/', response_model=List[FinanceiroFluxoCaixaResponse])
async def get_planos_conta(db: AsyncSession = Depends(get_session)):
    return await FinanceiroFluxoCaixaService.get_all(db)


@router.post('/', response_model=FinanceiroFluxoCaixaResponse, status_code=201)
async def post_plano_conta(payload: FinanceiroFluxoCaixaCreate, db: AsyncSession = Depends(get_session)):
    return await FinanceiroFluxoCaixaService.create(payload, db)


@router.get('/{id}', response_model=FinanceiroFluxoCaixaResponse)
async def get_plano_conta(id: int, db: AsyncSession = Depends(get_session)):
    return await FinanceiroFluxoCaixaService.get_by_id(id, db)


@router.put('/{id}', response_model=FinanceiroFluxoCaixaResponse)
async def put_plano_conta(id: int, payload: FinanceiroFluxoCaixaCreate, db: AsyncSession = Depends(get_session)):
    return await FinanceiroFluxoCaixaService.update(id, payload, db)


@router.delete('/{id}', status_code=204)
async def delete_plano_conta(id: int, db: AsyncSession = Depends(get_session)):
    return await FinanceiroFluxoCaixaService.delete(id, db)
