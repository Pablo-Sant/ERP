from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from schemas.fiscal_notas_fiscais import FiscalNotasFiscaisCreate, FiscalNotasFiscaisResponse
from services.fiscal_nota_fiscal_service import FiscalNotasFiscaisService

router = APIRouter()


@router.get('/', response_model=List[FiscalNotasFiscaisResponse])
async def get_planos_conta(db: AsyncSession = Depends(get_session)):
    return await FiscalNotasFiscaisService.get_all(db)


@router.post('/', response_model=FiscalNotasFiscaisResponse, status_code=201)
async def post_plano_conta(payload: FiscalNotasFiscaisCreate, db: AsyncSession = Depends(get_session)):
    return await FiscalNotasFiscaisService.create(payload, db)


@router.get('/{id}', response_model=FiscalNotasFiscaisResponse)
async def get_plano_conta(id: int, db: AsyncSession = Depends(get_session)):
    return await FiscalNotasFiscaisService.get_by_id(id, db)


@router.put('/{id}', response_model=FiscalNotasFiscaisResponse)
async def put_plano_conta(id: int, payload: FiscalNotasFiscaisCreate, db: AsyncSession = Depends(get_session)):
    return await FiscalNotasFiscaisService.update(id, payload, db)


@router.delete('/{id}', status_code=204)
async def delete_plano_conta(id: int, db: AsyncSession = Depends(get_session)):
    return await FiscalNotasFiscaisService.delete(id, db)
