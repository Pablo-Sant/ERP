from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.vc_cliente_final_model import ClienteFinal
from schemas.vc_cliente_final_schema import ClienteFinalResponse
from schemas.vc_cliente_final_schema import ClienteFinalCreate

router = APIRouter()

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ClienteFinalResponse])
async def get_cliente_final(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ClienteFinal)
        result = await session.execute(query)
        clientes:List[ClienteFinal] = result.scalars().all()
        
        return clientes
    
    
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ClienteFinalResponse)
async def post_cliente(cliente:ClienteFinalCreate, db:AsyncSession = Depends(get_session)):
    novo_cliente = ClienteFinal(
        nome = cliente.nome,
        cpf_cnpj = cliente.cpf_cnpj,
        email = cliente.email,
        telefone = cliente.telefone,
        endereco = cliente.endereco,
        cidade = cliente.cidade,
        data_ultima_compra = cliente.data_ultima_compra,
        valor_compra = cliente.valor_compra
    )
    
    db.add(novo_cliente)
    await db.commit()
    await db.refresh(novo_cliente)
    
    return novo_cliente


@router.get('/{id}', response_model=ClienteFinalResponse, status_code=status.HTTP_200_OK)
async def get_cliente(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ClienteFinal).filter(ClienteFinal.id == id)
        result = await session.execute(query)
        cliente = result.scalar_one_or_none()
        
        if cliente:
            return cliente
        else:
            raise HTTPException(detail='Cliente não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        

@router.put('/{id}', response_model=ClienteFinalResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_cliente(cliente:ClienteFinalCreate, id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ClienteFinal).filter(ClienteFinal.id == id)
        result = await session.execute(query)
        cliente_up = result.scalar_one_or_none()
        
        if cliente_up:
            cliente_up.nome = cliente.nome,
            cliente_up.cpf_cnpj = cliente.cpf_cnpj,
            cliente_up.email = cliente.email,
            cliente_up.telefone = cliente.telefone,
            cliente_up.endereco = cliente.endereco,
            cliente_up.cidade = cliente.cidade,
            cliente_up.data_ultima_compra = cliente.data_ultima_compra,
            cliente_up.valor_compra = cliente.valor_compra
            
            await session.commit()
            await session.refresh(cliente_up)
            
            return cliente_up
        
        else:
            raise HTTPException(detail='Cliente não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
        
        
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ClienteFinal).filter(ClienteFinal.id == id)
        result = await session.execute(query)
        cliente = result.scalar_one_or_none()
        
        if cliente:
            await session.delete(cliente)
            await session.commit()
            
            return Response(status_code = status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Cliente não encontrado', status_code=status.HTTP_404_NOT_FOUND)
            
            