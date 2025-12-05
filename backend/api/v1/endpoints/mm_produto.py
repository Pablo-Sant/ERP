from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from schemas.mm_produto_schema import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from services.mm_produto_service import ProdutoService

router = APIRouter()



@router.get('/', response_model=List[ProdutoResponse])
async def get_planos_conta(db: AsyncSession = Depends(get_session)):
    return await ProdutoService.get_all(db)


@router.post('/', response_model=ProdutoResponse, status_code=201)
async def post_plano_conta(payload: ProdutoCreate, db: AsyncSession = Depends(get_session)):
    return await ProdutoService.criar(payload, db)


@router.get('/{id}', response_model=ProdutoResponse)
async def get_plano_conta(id: int, db: AsyncSession = Depends(get_session)):
    return await ProdutoService.get_by_id(id, db)


@router.put('/{id}', response_model=ProdutoResponse, status_code=200)
async def put_plano_conta(id: int, payload: ProdutoUpdate, db: AsyncSession = Depends(get_session)):
    return await ProdutoService.update(id, payload, db)


@router.delete('/{id}', status_code=204)
async def delete_plano_conta(id: int, db: AsyncSession = Depends(get_session)):
    await ProdutoService.get_all(db)

    return Response(status_code=204)
