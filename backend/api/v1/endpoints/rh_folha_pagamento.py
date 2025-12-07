from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.rh_folha_pagamento_model import FolhaPagamento
from schemas.rh_folha_pagamento_schema import FolhaPagamentoCreate, FolhaPagamentoResponse

router = APIRouter()

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[FolhaPagamentoResponse])
async def get_cliente_final(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(FolhaPagamento)
        result = await session.execute(query)
        colaborador:List[FolhaPagamento] = result.scalars().all()
        
        return colaborador
    
    
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=FolhaPagamentoResponse)
async def post_cliente(folha_pagamento:FolhaPagamentoCreate, db:AsyncSession = Depends(get_session)):
    nova_folha_pagamento = FolhaPagamento(
        colaborador_id = folha_pagamento.colaborador_id,
        mes = folha_pagamento.mes,
        ano = folha_pagamento.ano,
        salario_base = folha_pagamento.salario_base,
        descontos = folha_pagamento.descontos,
        salario_liquido = folha_pagamento.salario_liquido
    )
    
    db.add(nova_folha_pagamento)
    await db.commit()
    await db.refresh(nova_folha_pagamento)
    
    return nova_folha_pagamento


@router.get('/{id}', response_model=FolhaPagamentoResponse, status_code=status.HTTP_200_OK)
async def get_cliente(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(FolhaPagamento).filter(FolhaPagamento.id == id)
        result = await session.execute(query)
        folha_pagamento = result.scalar_one_or_none()
        
        if folha_pagamento:
            return folha_pagamento
        else:
            raise HTTPException(detail='Folha de pagamento não encontrada', status_code=status.HTTP_404_NOT_FOUND)
        

@router.put('/{id}', response_model=FolhaPagamentoResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_cliente(colaborador:FolhaPagamentoCreate, id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(FolhaPagamento).filter(FolhaPagamento.id == id)
        result = await session.execute(query)
        folha_pagamento = result.scalar_one_or_none()
        
        if folha_pagamento:
            folha_pagamento.colaborador_id = folha_pagamento.colaborador_id,
            folha_pagamento.data_avaliacao = folha_pagamento.data_avaliacao,
            folha_pagamento.ano = colaborador.ano,
            folha_pagamento.salario_base = folha_pagamento.salario_base,
            folha_pagamento.descontos = folha_pagamento.descontos,
            folha_pagamento.salario_liquido = folha_pagamento.salario_liquido
            
            await session.commit()
            await session.refresh(colaborador)
            
            return colaborador
        
        else:
            raise HTTPException(detail='Folha de pagamento   não encontrada', status_code=status.HTTP_404_NOT_FOUND)
        
        
        
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(FolhaPagamento).filter(FolhaPagamento.id == id)
        result = await session.execute(query)
        colaborador = result.scalar_one_or_none()
        
        if colaborador:
            await session.delete(colaborador)
            await session.commit()
            
            return Response(status_code = status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Folha de pagamento não encontrada', status_code=status.HTTP_404_NOT_FOUND)
            
            