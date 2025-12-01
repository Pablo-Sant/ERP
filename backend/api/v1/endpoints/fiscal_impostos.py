from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.fiscal_impostos import FiscalImpostos
from schemas.fiscal_impostos import FiscalImpostosCreate, FiscalImpostosResponse

router = APIRouter()


async def get_plano_conta_or_404(id: int, db: AsyncSession):
    query = select(FiscalImpostos).filter(FiscalImpostos.id_imposto == id)
    result = await db.execute(query)
    obj = result.scalar_one_or_none()

    if not obj:
        raise HTTPException(status_code=404, detail="Documento ativo não encontrado")
    return obj


@router.get('/', response_model=List[FiscalImpostosResponse])
async def get_planos_conta(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(FiscalImpostos))
    return result.scalars().all()


@router.post('/', response_model=FiscalImpostosResponse, status_code=201)
async def post_plano_conta(payload: FiscalImpostosCreate, db: AsyncSession = Depends(get_session)):
    novo = FiscalImpostos(**payload.model_dump())
    db.add(novo)

    await db.commit()
    await db.refresh(novo)

    return novo


@router.get('/{id}', response_model=FiscalImpostosResponse)
async def get_plano_conta(id: int, db: AsyncSession = Depends(get_session)):
    return await get_plano_conta_or_404(id, db)


@router.put('/{id}', response_model=FiscalImpostos)
async def put_plano_conta(id: int, payload: FiscalImpostosCreate, db: AsyncSession = Depends(get_session)):
    plano = await get_plano_conta_or_404(id, db)
    data = payload.model_dump()

    
    for attr, value in data.items():
        setattr(plano, attr, value)

    await db.commit()
    await db.refresh(plano)

    return plano


@router.delete('/{id}', status_code=204)
async def delete_plano_conta(id: int, db: AsyncSession = Depends(get_session)):
    plano = await get_plano_conta_or_404(id, db)

    await db.delete(plano)
    await db.commit()

    return Response(status_code=204)
