from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from schemas.rh_avaliacao_desempenho_schema import AvaliacaoDesempenhoCreate
from schemas.rh_avaliacao_desempenho_schema import AvaliacaoDesempenhoRead
from services.rh_avaliacao_desempenho_service import AvaliacaoDesempenhoService

router = APIRouter()

@router.get('/', status=200, response_model=AvaliacaoDesempenhoRead)
async def get_all(db: AsyncSession = Depends(get_session)):
    return AvaliacaoDesempenhoService.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AvaliacaoDesempenhoRead)
async def post_cliente(colaborador:AvaliacaoDesempenhoCreate, db:AsyncSession = Depends(get_session)):
    return AvaliacaoDesempenhoService.post(colaborador, db)


@router.get('/{id}', response_model=AvaliacaoDesempenhoRead, status_code=status.HTTP_200_OK)
async def get_cliente(db:AsyncSession = Depends(get_session)):
    return AvaliacaoDesempenhoService.get_by_id(id, db)
        

@router.put('/{id}', response_model=AvaliacaoDesempenhoRead, status_code=status.HTTP_202_ACCEPTED)
async def put_cliente(colaborador:AvaliacaoDesempenhoCreate, id:int, db:AsyncSession = Depends(get_session)):
    return AvaliacaoDesempenhoService.update(id, colaborador, db)
        
               
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id:int, db:AsyncSession = Depends(get_session)):
    return AvaliacaoDesempenhoService.delete(id, db)
            
            