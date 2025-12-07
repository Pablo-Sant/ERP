from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.rh_funcoes_model import Funcao
from schemas.rh_funcoes_schema import FuncaoCreate, FuncaoResponse, FuncaoUpdate

router = APIRouter()

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[FuncaoResponse])
async def get_cliente_final(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Funcao)
        result = await session.execute(query)
        colaborador:List[Funcao] = result.scalars().all()
        
        return colaborador
    
    
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=FuncaoResponse)
async def post_cliente(folha_pagamento:FuncaoCreate, db:AsyncSession = Depends(get_session)):
    nova_folha_pagamento = Funcao(
        nome = folha_pagamento.nome,
        descricao = folha_pagamento.descricao,
        colaboradores = folha_pagamento.colaboradores
    )
    
    db.add(nova_folha_pagamento)
    await db.commit()
    await db.refresh(nova_folha_pagamento)
    
    return nova_folha_pagamento


@router.get('/{id}', response_model=FuncaoResponse, status_code=status.HTTP_200_OK)
async def get_cliente(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Funcao).filter(Funcao.id == id)
        result = await session.execute(query)
        folha_pagamento = result.scalar_one_or_none()
        
        if folha_pagamento:
            return folha_pagamento
        else:
            raise HTTPException(detail='Folha de pagamento não encontrada', status_code=status.HTTP_404_NOT_FOUND)
        

@router.put('/{id}', response_model=FuncaoResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_cliente(colaborador:FuncaoCreate, id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Funcao).filter(Funcao.id == id)
        result = await session.execute(query)
        folha_pagamento = result.scalar_one_or_none()
        
        if folha_pagamento:
            folha_pagamento.nome = folha_pagamento.nome,
            folha_pagamento.descricao = folha_pagamento.descricao,
            folha_pagamento.colaboradores = folha_pagamento.colaboradores
            
            await session.commit()
            await session.refresh(colaborador)
            
            return colaborador
        
        else:
            raise HTTPException(detail='Folha de pagamento   não encontrada', status_code=status.HTTP_404_NOT_FOUND)
        
        
        
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Funcao).filter(Funcao.id == id)
        result = await session.execute(query)
        colaborador = result.scalar_one_or_none()
        
        if colaborador:
            await session.delete(colaborador)
            await session.commit()
            
            return Response(status_code = status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Folha de pagamento não encontrada', status_code=status.HTTP_404_NOT_FOUND)
            
            