from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from schemas.peca_ordem_servico_schema import PecasOrdemServicoResponse, PecasOrdemServicoCreate
from services.pecas_ordem_servico_service import PecasOrdemServicoService

router = APIRouter()

@router.get("/", response_model=List[PecasOrdemServicoResponse])
async def listar(db: AsyncSession = Depends(get_session)):
    return await PecasOrdemServicoService.listar(db)


@router.post("/", response_model=PecasOrdemServicoResponse, status_code=status.HTTP_201_CREATED)
async def criar(dto: PecasOrdemServicoCreate, db: AsyncSession = Depends(get_session)):
    return await PecasOrdemServicoService.criar(dto, db)


@router.get("/{id}", response_model=PecasOrdemServicoResponse)
async def obter(id: int, db: AsyncSession = Depends(get_session)):
    return await PecasOrdemServicoService.obter_por_id(id, db)


@router.put("/{id}", response_model=PecasOrdemServicoResponse)
async def atualizar(id: int, dto: PecasOrdemServicoCreate, db: AsyncSession = Depends(get_session)):
    return await PecasOrdemServicoService.atualizar(id, dto, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar(id: int, db: AsyncSession = Depends(get_session)):
    await PecasOrdemServicoService.deletar(id, db)
    return None
