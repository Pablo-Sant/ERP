from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session


from schemas.fiscal_impostos import FiscalImpostosCreate, FiscalImpostosResponse
from services.fiscal_imposto_service import FiscalImpostosService

router = APIRouter()


@router.get('/', response_model=List[FiscalImpostosResponse])
async def get_planos_conta(db: AsyncSession = Depends(get_session)):
    return await FiscalImpostosService.get_all(db)


@router.post('/', response_model=FiscalImpostosResponse, status_code=201)
async def post_plano_conta(payload: FiscalImpostosCreate, db: AsyncSession = Depends(get_session)):
    return await FiscalImpostosService.create(payload, db)


@router.get('/{id}', response_model=FiscalImpostosResponse)
async def get_plano_conta(id: int, db: AsyncSession = Depends(get_session)):
    return await FiscalImpostosService.get_by_id(id, db)


@router.put('/{id}', response_model=FiscalImpostosResponse)
async def put_plano_conta(id: int, payload: FiscalImpostosCreate, db: AsyncSession = Depends(get_session)):
    return await FiscalImpostosService.update(id, payload, db)


@router.delete('/{id}', status_code=204)
async def delete_plano_conta(id: int, db: AsyncSession = Depends(get_session)):
    return await FiscalImpostosService.delete(id, db)
