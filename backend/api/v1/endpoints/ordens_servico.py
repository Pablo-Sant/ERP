from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.ordens_servicos_model import OrdemServico
from schemas.ordem_servico_schema import OrdemServicoCreate, OrdemServicoResponse

router = APIRouter()


async def get_plano_conta_or_404(id: int, db: AsyncSession):
    query = select(OrdemServico).filter(OrdemServico.id == id)
    result = await db.execute(query)
    obj = result.scalar_one_or_none()

    if not obj:
        raise HTTPException(status_code=404, detail="Ordem Servico não encontrado")
    return obj


@router.get('/', response_model=List[OrdemServicoResponse])
async def get_planos_conta(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(OrdemServico))
    return result.scalars().all()


@router.post('/', response_model=OrdemServicoResponse, status_code=201)
async def post_plano_conta(payload: OrdemServicoCreate, db: AsyncSession = Depends(get_session)):
    novo = OrdemServico(**payload.model_dump())
    db.add(novo)

    await db.commit()
    await db.refresh(novo)

    return novo


@router.get('/{id}', response_model=OrdemServicoResponse)
async def get_plano_conta(id: int, db: AsyncSession = Depends(get_session)):
    return await get_plano_conta_or_404(id, db)


@router.put('/{id}', response_model=OrdemServicoResponse)
async def put_plano_conta(id: int, payload: OrdemServicoCreate, db: AsyncSession = Depends(get_session)):
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
