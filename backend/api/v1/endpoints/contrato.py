from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from schemas.vc_contrato_schema import ContratoCreate, ContratoResponse
from models.vc_contrato_model import Contrato

router = APIRouter()

@router.get('/', status_code = status.HTTP_200_OK, response_model=List[ContratoResponse])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Contrato)
        result = await session.execute(query)
        contratos:List[Contrato] = result.scalars().all()
        
        return contratos
    
@router.post('/{id}', status_code = status.HTTP_201_CREATED, response_model=ContratoResponse)
async def post_curso(id:int, contrato:ContratoCreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        novo_contrato = Contrato(
            cliente_finalid = contrato.cliente_finalid,
            vendedorid = contrato.vendedorid,
            data_inicio = contrato.data_inicio,
            vencimento = contrato.vencimento,
            
        )
        
        db.add(novo_contrato)
        db.commit()
        db.refresh(novo_contrato)
        
        return novo_contrato
    

@router.get('/{id}', response_model=ContratoResponse, status_code=status.HTTP_200_OK)
async def get_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Contrato).filter(Contrato.contratoid == id)
        result = await session.execute(query)
        contrato = result.scalar_one_or_none()
        
        if contrato:
            return contrato
        else:
            raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id}', response_model=ContratoResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_produto(id:int, produto:ContratoCreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Contrato).filter(Contrato.contratoid == id)
        result = await session.execute(query)
        contrato = result.scalar_one_or_none()
        
        if contrato:
            contrato.cliente_finalid = contrato.cliente_finalid,
            contrato.vendedorid = contrato.vendedorid,
            contrato.data_inicio = contrato.data_inicio,
            contrato.vencimento = contrato.vencimento
            
            return contrato
        
        else:
            raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Contrato).filter(Contrato.contratoid == id)
        result = await session.execute(query)
        contrato = result.scalar_one_or_none()
        
        if contrato:
            await session.delete(contrato)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)
   