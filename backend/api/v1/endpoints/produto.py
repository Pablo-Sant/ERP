from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from schemas.mm_produto_schema import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from models.mm_produto_model import Produto

router = APIRouter()

@router.get('/', status_code = status.HTTP_200_OK, response_model=List[ProdutoResponse])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Produto)
        result = await session.execute(query)
        produtos:List[Produto] = result.scalars().all()
        
        return produtos 
    
@router.post('/{id}', status_code = status.HTTP_201_CREATED, response_model=ProdutoResponse)
async def post_curso(id:int, produto:ProdutoCreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        novo_produto = Produto(
            empresa_id = produto.empresa_id,
            categoria_id = produto.categoria_id,
            nome = produto.nome,
            descricao = produto.descricao,
            data_criacao = produto.data_criacao,
            data_atualizacao = produto.data_atualizacao
        )
        
        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)
        
        return novo_produto
    

@router.get('/{id}', response_model=ProdutoResponse, status_code=status.HTTP_200_OK)
async def get_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Produto).filter(Produto.id == id)
        result = await session.execute(query)
        produto = result.scalar_one_or_none()
        
        if produto:
            return produto
        else:
            raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id}', response_model=ProdutoResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_produto(id:int, produto:ProdutoCreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Produto).filter(Produto.id == id)
        result = await session.execute(query)
        produto = result.scalar_one_or_none()
        
        if produto:
            produto.empresa_id = produto.empresa_id,
            produto.categoria_id = produto.categoria_id,
            produto.nome = produto.nome,
            produto.descricao = produto.descricao,
            produto.data_criacao = produto.data_atualizacao,
            produto.data_atualizacao = produto.data_atualizacao
            
            return produto
        
        else:
            raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Produto).filter(Produto.id == id)
        result = await session.execute(query)
        produto = result.scalar_one_or_none()
        
        if produto:
            await session.delete(produto)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)
   