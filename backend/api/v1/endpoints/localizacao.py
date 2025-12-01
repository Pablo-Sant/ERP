from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from schemas.localizacao_schema import LocalizacaoCreate, LocalizacaoResponse
from models.localizacao_model import Localizacao

router = APIRouter()

@router.get('/', status_code = status.HTTP_200_OK, response_model=List[LocalizacaoResponse])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Localizacao)
        result = await session.execute(query)
        localizacao:List[Localizacao] = result.scalars().all()
        
        return localizacao
    
@router.post('/{id}', status_code = status.HTTP_201_CREATED, response_model=LocalizacaoResponse)
async def post_curso(id:int, localizacao:LocalizacaoCreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        nova_localizacao = Localizacao(
            codigo = localizacao.codigo,
            nome = localizacao.nome,
            tipo_local = localizacao.tipo_local,
            endereco = localizacao.endereco,
            latitude = localizacao.latitude,
            longitude = localizacao.longitude,
            pessoa_contato = localizacao.pessoa_contato,
            telefone_contato = localizacao.telefone_contato,
            ativo = localizacao.ativo
        )
        
        db.add(nova_localizacao)
        db.commit()
        db.refresh(nova_localizacao)
        
        return nova_localizacao
    

@router.get('/{id}', response_model=LocalizacaoResponse, status_code=status.HTTP_200_OK)
async def get_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Localizacao).filter(Localizacao.id == id)
        result = await session.execute(query)
        localizacao = result.scalar_one_or_none()
        
        if localizacao:
            return localizacao
        else:
            raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id}', response_model=LocalizacaoResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_produto(id:int, localizacao:LocalizacaoCreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Localizacao).filter(Localizacao.id == id)
        result = await session.execute(query)
        localizacao = result.scalar_one_or_none()
        
        if localizacao:
            localizacao.codigo = localizacao.codigo,
            localizacao.nome = localizacao.nome,
            localizacao.tipo_local = localizacao.tipo_local,
            localizacao.endereco = localizacao.endereco,
            localizacao.latitude = localizacao.latitude,
            localizacao.longitude = localizacao.longitude,
            localizacao.pessoa_contato = localizacao.pessoa_contato,
            localizacao.telefone_contato = localizacao.telefone_contato,
            localizacao.ativo = localizacao.ativo
            
            return localizacao
        
        else:
            raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Localizacao).filter(Localizacao.id == id)
        result = await session.execute(query)
        localizacao = result.scalar_one_or_none()
        
        if localizacao:
            await session.delete(localizacao)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)
   