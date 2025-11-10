from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.cliente_model import ClienteModel
from schemas.cliente_schema import ClientesSchema
from core.deps import get_session

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ClientesSchema)
async def post_clente(cliente:ClientesSchema, db:AsyncSession = Depends(get_session)):
    novo_cliente = ClienteModel(Nome="aaa", Email="aaaa@gmail.com")
    
    db.add(novo_cliente)
    await db.commit()
    
    return novo_cliente


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ClientesSchema])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ClienteModel)
        result = await session.execute(query)
        clientes: List[ClienteModel] = result.scalars().all()
        
        return clientes
    