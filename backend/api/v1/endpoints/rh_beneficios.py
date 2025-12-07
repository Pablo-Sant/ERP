from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.rh_beneficios_model import Beneficio
from schemas.rh_beneficios_schema import BeneficioCreate, BeneficioResponse

router = APIRouter()

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[BeneficioResponse])
async def get_cliente_final(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Beneficio)
        result = await session.execute(query)
        colaborador:List[Beneficio] = result.scalars().all()
        
        return colaborador
    
    
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=BeneficioResponse)
async def post_cliente(colaborador:BeneficioCreate, db:AsyncSession = Depends(get_session)):
    nova_avaliacao_desempenho = Beneficio(
        nome = colaborador.nome,
        descricao = colaborador.descricao,
        valor = colaborador.valor
        
    )
    
    db.add(nova_avaliacao_desempenho)
    await db.commit()
    await db.refresh(nova_avaliacao_desempenho)
    
    return nova_avaliacao_desempenho


@router.get('/{id}', response_model=BeneficioResponse, status_code=status.HTTP_200_OK)
async def get_cliente(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Beneficio).filter(Beneficio.id == id)
        result = await session.execute(query)
        avaliacao_desempenho = result.scalar_one_or_none()
        
        if avaliacao_desempenho:
            return avaliacao_desempenho
        else:
            raise HTTPException(detail='Beneficio não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        

@router.put('/{id}', response_model=BeneficioResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_cliente(colaborador:BeneficioCreate, id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Beneficio).filter(Beneficio.id == id)
        result = await session.execute(query)
        colaborador = result.scalar_one_or_none()
        
        if colaborador:
            colaborador.nome = colaborador.nome,
            colaborador.descricao = colaborador.descricao,
            colaborador.valor = colaborador.valor
                        
            await session.commit()
            await session.refresh(colaborador)
            
            return colaborador
        
        else:
            raise HTTPException(detail='Benefício não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
        
        
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Beneficio).filter(Beneficio.id == id)
        result = await session.execute(query)
        colaborador = result.scalar_one_or_none()
        
        if colaborador:
            await session.delete(colaborador)
            await session.commit()
            
            return Response(status_code = status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Benefício não encontrado', status_code=status.HTTP_404_NOT_FOUND)
            
            