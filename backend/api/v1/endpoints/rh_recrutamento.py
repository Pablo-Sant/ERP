from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.rh_recrutamento_model import Recrutamento
from schemas.rh_recrutamento_schema import RecrutamentoCreate, RecrutamentoResponse

router = APIRouter()

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[RecrutamentoResponse])
async def get_cliente_final(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Recrutamento)
        result = await session.execute(query)
        colaborador:List[Recrutamento] = result.scalars().all()
        
        return colaborador
    
    
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=RecrutamentoResponse)
async def post_cliente(folha_pagamento:RecrutamentoCreate, db:AsyncSession = Depends(get_session)):
    nova_folha_pagamento = Recrutamento(
        colaborador_id = folha_pagamento.colaborador_id,
        data_recrutamento = folha_pagamento.data_recrutamento,
        status = folha_pagamento.status,
        observacoes = folha_pagamento.observacoes
    )
    
    db.add(nova_folha_pagamento)
    await db.commit()
    await db.refresh(nova_folha_pagamento)
    
    return nova_folha_pagamento


@router.get('/{id}', response_model=RecrutamentoResponse, status_code=status.HTTP_200_OK)
async def get_cliente(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Recrutamento).filter(Recrutamento.id == id)
        result = await session.execute(query)
        folha_pagamento = result.scalar_one_or_none()
        
        if folha_pagamento:
            return folha_pagamento
        else:
            raise HTTPException(detail='Recrutamento não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        

@router.put('/{id}', response_model=RecrutamentoResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_cliente(colaborador:RecrutamentoCreate, id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Recrutamento).filter(Recrutamento.id == id)
        result = await session.execute(query)
        folha_pagamento = result.scalar_one_or_none()
        
        if folha_pagamento:
            folha_pagamento.colaborador_id = folha_pagamento.colaborador_id,
            folha_pagamento.data_recrutamento = folha_pagamento.data_recrutamento,
            folha_pagamento.status = colaborador.status,
            folha_pagamento.observacoes = folha_pagamento.observacoes

            await session.commit()
            await session.refresh(colaborador)
            
            return colaborador
        
        else:
            raise HTTPException(detail='Recrutamento não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
        
        
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Recrutamento).filter(Recrutamento.id == id)
        result = await session.execute(query)
        colaborador = result.scalar_one_or_none()
        
        if colaborador:
            await session.delete(colaborador)
            await session.commit()
            
            return Response(status_code = status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Recrutamento não encontrado', status_code=status.HTTP_404_NOT_FOUND)
            
            