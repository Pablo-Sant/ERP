from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.am_planos_manutencao_model import PlanosManutencao
from schemas.planos_manutencao_schema import PlanosManutencaoResponse, PlanosManutencaoCreate
from services.planos_manutencao_service import PlanosManutencaoService

router = APIRouter()

@router.get('/', status_code = status.HTTP_200_OK, response_model=List[PlanosManutencaoResponse])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    return await PlanosManutencaoService.listar(db)
    
@router.post('/{id}', status_code = status.HTTP_201_CREATED, response_model=PlanosManutencaoResponse)
async def post_curso(id:int, plano_manutencao:PlanosManutencaoCreate, db: AsyncSession = Depends(get_session)):
    PlanosManutencaoService.criar(plano_manutencao, db)
    

@router.get('/{id}', response_model=PlanosManutencaoResponse, status_code=status.HTTP_200_OK)
async def get_produto(id:int, db: AsyncSession = Depends(get_session)):
    return await PlanosManutencaoService.obter_por_id(id, db)


@router.put('/{id}', response_model=PlanosManutencaoResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_produto(id:int, planos_manutencao:PlanosManutencaoCreate, db: AsyncSession = Depends(get_session)):
    return await PlanosManutencaoService.atualizar(id, planos_manutencao, db)
        

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_produto(id:int, db: AsyncSession = Depends(get_session)):
    await PlanosManutencaoService.deletar(id, db)
    return None