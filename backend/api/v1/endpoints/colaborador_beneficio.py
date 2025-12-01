from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.rh_colaborador_beneficio_model import ColaboradorBeneficio
from schemas.rh_colaborador_beneficio_schema import ColaboradorBeneficioCreate, ColaboradorBeneficioRead

router = APIRouter()

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ColaboradorBeneficioRead])
async def get_cliente_final(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ColaboradorBeneficio)
        result = await session.execute(query)
        colaborador:List[ColaboradorBeneficio] = result.scalars().all()
        
        return colaborador
    
    
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ColaboradorBeneficioRead)
async def post_cliente(colaborador:ColaboradorBeneficioCreate, db:AsyncSession = Depends(get_session)):
    novo_colaborador = ColaboradorBeneficio(
        colaborador_id = colaborador.colaborador_id,
        beneficio_id = colaborador.beneficio_id
    )
    
    db.add(novo_colaborador)
    await db.commit()
    await db.refresh(novo_colaborador)
    
    return novo_colaborador


@router.get('/{id}', response_model=ColaboradorBeneficioRead, status_code=status.HTTP_200_OK)
async def get_cliente(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ColaboradorBeneficio).filter(ColaboradorBeneficio.id == id)
        result = await session.execute(query)
        colaborador = result.scalar_one_or_none()
        
        if colaborador:
            return colaborador
        else:
            raise HTTPException(detail='Colaborador não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        

@router.put('/{id}', response_model=ColaboradorBeneficioRead, status_code=status.HTTP_202_ACCEPTED)
async def put_cliente(colaborador:ColaboradorBeneficioCreate, id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ColaboradorBeneficio).filter(ColaboradorBeneficio.id == id)
        result = await session.execute(query)
        colaborador = result.scalar_one_or_none()
        
        if colaborador:
            colaborador.colaborador_id = colaborador.colaborador_id,
            colaborador.beneficio_id = colaborador.beneficio_id,

            
            await session.commit()
            await session.refresh(colaborador)
            
            return colaborador
        
        else:
            raise HTTPException(detail='Colaborador não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
        
        
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ColaboradorBeneficio).filter(ColaboradorBeneficio.id == id)
        result = await session.execute(query)
        colaborador = result.scalar_one_or_none()
        
        if colaborador:
            await session.delete(colaborador)
            await session.commit()
            
            return Response(status_code = status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Colaborador não encontrado', status_code=status.HTTP_404_NOT_FOUND)
            
            