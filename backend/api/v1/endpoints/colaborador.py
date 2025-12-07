from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.rh_colaboradores_model import Colaborador
from schemas.rh_colaborador_schema import ColaboradorCreate, ColaboradorResponse

router = APIRouter()

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ColaboradorResponse])
async def get_cliente_final(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Colaborador)
        result = await session.execute(query)
        colaborador:List[Colaborador] = result.scalars().all()
        
        return colaborador
    
    
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ColaboradorResponse)
async def post_cliente(colaborador:ColaboradorCreate, db:AsyncSession = Depends(get_session)):
    novo_colaborador = Colaborador(
        nome = colaborador.nome,
        cpf = colaborador.cpf,
        email = colaborador.email,
        funcao_id = colaborador.funcao_id,
        data_contratacao = colaborador.data_contratacao,
        carga_horaria = colaborador.carga_horaria,
        data_nascimento = colaborador.data_de_nascimento,
        data_recrutamento = colaborador.data_de_recrutamento,
        salario = colaborador.salario
    )
    
    db.add(novo_colaborador)
    await db.commit()
    await db.refresh(novo_colaborador)
    
    return novo_colaborador


@router.get('/{id}', response_model=ColaboradorResponse, status_code=status.HTTP_200_OK)
async def get_cliente(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Colaborador).filter(Colaborador.id == id)
        result = await session.execute(query)
        colaborador = result.scalar_one_or_none()
        
        if colaborador:
            return colaborador
        else:
            raise HTTPException(detail='Colaborador não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        

@router.put('/{id}', response_model=ColaboradorResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_cliente(colaborador:ColaboradorCreate, id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Colaborador).filter(Colaborador.id == id)
        result = await session.execute(query)
        colaborador = result.scalar_one_or_none()
        
        if colaborador:
            colaborador.nome = colaborador.nome,
            colaborador.cpf = colaborador.cpf_cnpj,
            colaborador.email = colaborador.email,
            colaborador.funcao_id = colaborador.funcao_id,
            colaborador.data_contratacao = colaborador.data_contratacao,
            colaborador.carga_horaria = colaborador.carga_horaria,
            colaborador.data_de_nascimento = colaborador.data_de_nascimento,
            colaborador.data_de_recrutamento = colaborador.data_de_recrutamento
            
            await session.commit()
            await session.refresh(colaborador)
            
            return colaborador
        
        else:
            raise HTTPException(detail='Colaborador não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
        
        
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Colaborador).filter(Colaborador.id == id)
        result = await session.execute(query)
        colaborador = result.scalar_one_or_none()
        
        if colaborador:
            await session.delete(colaborador)
            await session.commit()
            
            return Response(status_code = status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Colaborador não encontrado', status_code=status.HTTP_404_NOT_FOUND)
            
            