from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.financeiro_conta import FinanceiroContas
from schemas.financeiro_contas_financeiras import FinanceiroContasCreate, FinanceiroContasResponse
from services.financeiro_conta_service import FinanceiroContaService


router = APIRouter()


@router.get('/', response_model=List[FinanceiroContasResponse])
async def get_planos_conta(db: AsyncSession = Depends(get_session)):
    return await FinanceiroContaService.listar(db)


@router.post('/', response_model=FinanceiroContasResponse, status_code=201)
async def post_plano_conta(payload: FinanceiroContasCreate, db: AsyncSession = Depends(get_session)):
    return await FinanceiroContaService.criar(payload, db)


@router.get('/{id}', response_model=FinanceiroContasResponse)
async def get_plano_conta(id: int, db: AsyncSession = Depends(get_session)):
    return await FinanceiroContaService.obter_por_id(id, db)


@router.put('/{id}', response_model=FinanceiroContas)
async def put_plano_conta(id: int, payload: FinanceiroContasCreate, db: AsyncSession = Depends(get_session)):
    return await FinanceiroContaService.atualizar(id, payload, db)


@router.delete('/{id}', status_code=204)
async def delete_plano_conta(id: int, db: AsyncSession = Depends(get_session)):
    await FinanceiroContaService.deletar(id, db)
    return None
