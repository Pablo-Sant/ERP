from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from schemas.ativo_schema import AtivoCreate, AtivoResponse
from models.ativos_model import Ativo

router = APIRouter()

@router.get('/', status_code = status.HTTP_200_OK, response_model=List[AtivoResponse])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Ativo)
        result = await session.execute(query)
        ativos:List[Ativo] = result.scalars().all()
        
        return ativos
    
@router.post('/{id}', status_code = status.HTTP_201_CREATED, response_model=AtivoResponse)
async def post_curso(id:int, ativo:AtivoCreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        novo_ativo = Ativo(
            id_categoria = ativo.id_categoria,
            id_localizacao = ativo.id_localizacao,
            numero_tag = ativo.numero_tag,
            numero_serie = ativo.numero_serie,
            modelo = ativo.modelo,
            fabricante = ativo.fabricante,
            nome = ativo.nome,
            descricao = ativo.descricao,
            status_ativo = ativo.status_ativo,
            criticidade = ativo.criticidade,
            data_aquisicao = ativo.data_aquisicao,
            custo_aquisicao = ativo.custo_aquisicao,
            numero_ordem_compra = ativo.numero_ordem_compra,
            id_fornecedor = ativo.id_fornecedor,
            data_vencimento_garantia = ativo.data_vencimento_garantia,
            valor_residual = ativo.valor_residual,
            valor_atual = ativo.valor_atual,
            especificacoes = ativo.especificacoes,
            parameros_tecnicos = ativo.parametros_tecnicos,
            vida_util_anos = ativo.vida_util_anos   
        )
        
        db.add(novo_ativo)
        db.commit()
        db.refresh(novo_ativo)
        
        return novo_ativo
    

@router.get('/{id}', response_model=AtivoResponse, status_code=status.HTTP_200_OK)
async def get_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Ativo).filter(Ativo.id == id)
        result = await session.execute(query)
        ativo = result.scalar_one_or_none()
        
        if ativo:
            return ativo
        else:
            raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id}', response_model=AtivoResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_produto(id:int, produto:AtivoCreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Ativo).filter(Ativo.id == id)
        result = await session.execute(query)
        ativo = result.scalar_one_or_none()
        
        if ativo:
            ativo.id_categoria = ativo.id_categoria,
            ativo.id_localizacao = ativo.id_localizacao,
            ativo.numero_tag = ativo.numero_tag,
            ativo.numero_serie = ativo.numero_serie,
            ativo.modelo = ativo.modelo,
            ativo.fabricante = ativo.fabricante,
            ativo.nome = ativo.nome,
            ativo.descricao = ativo.descricao,
            ativo.status_ativo = ativo.status_ativo,
            ativo.criticidade = ativo.criticidade,
            ativo.data_aquisicao = ativo.data_aquisicao,
            ativo.custo_aquisicao = ativo.custo_aquisicao,
            ativo.numero_ordem_compra = ativo.numero_ordem_compra,
            ativo.id_fornecedor = ativo.id_fornecedor,
            ativo.data_vencimento_garantia = ativo.data_vencimento_garantia,
            ativo.valor_residual = ativo.valor_residual,
            ativo.valor_atual = ativo.valor_atual,
            ativo.especificacoes = ativo.especificacoes,
            ativo.parameros_tecnicos = ativo.parametros_tecnicos,
            ativo.vida_util_anos = ativo.vida_util_anos
            
            return ativo
        
        else:
            raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Ativo).filter(Ativo.id == id)
        result = await session.execute(query)
        ativo = result.scalar_one_or_none()
        
        if ativo:
            await session.delete(ativo)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Produto não encontrado', status_code=status.HTTP_404_NOT_FOUND)
   