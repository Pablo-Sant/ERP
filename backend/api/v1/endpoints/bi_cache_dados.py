from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.bi_cache_dados_model import CacheDadosBI
from schemas.bi_cache_dados_schema import CacheDadosBIRead, CacheDadosBICreate

router = APIRouter()

@router.get('/', status_code = status.HTTP_200_OK, response_model=List[CacheDadosBIRead])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CacheDadosBI)
        result = await session.execute(query)
        ativos:List[CacheDadosBI] = result.scalars().all()
        
        return ativos
    
    
@router.post('/', status_code = status.HTTP_201_CREATED, response_model=CacheDadosBIRead)
async def post_curso(plano_manutencao:CacheDadosBICreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        novo_plano_manutencao = CacheDadosBI(
            chave_cache = plano_manutencao.chave_cache,
            dados_json = plano_manutencao.dados_json,
            data_geracao = plano_manutencao.data_geracao,
            data_expiracao = plano_manutencao.data_expiracao  
        )
        
        db.add(novo_plano_manutencao)
        db.commit()
        db.refresh(novo_plano_manutencao)
        
        return novo_plano_manutencao
    

@router.get('/{id}', response_model=CacheDadosBIRead, status_code=status.HTTP_200_OK)
async def get_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CacheDadosBI).filter(CacheDadosBI.id_cache == id)
        result = await session.execute(query)
        ativo = result.scalar_one_or_none()
        
        if ativo:
            return ativo
        else:
            raise HTTPException(detail='Cache Dados não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id}', response_model=CacheDadosBIRead, status_code=status.HTTP_202_ACCEPTED)
async def put_produto(id:int, plano_manutencao:CacheDadosBICreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CacheDadosBI).filter(CacheDadosBI.id_cache == id)
        result = await session.execute(query)
        registro_calibracao = result.scalar_one_or_none()
        
        if registro_calibracao:
            registro_calibracao.chave_cache = plano_manutencao.chave_cache,
            registro_calibracao.dados_json = plano_manutencao.dados_json,
            registro_calibracao.data_geracao = plano_manutencao.data_geracao,
            registro_calibracao.data_expiracao = plano_manutencao.data_expiracao
            
            return registro_calibracao
        
        else:
            raise HTTPException(detail='Cache BI não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CacheDadosBI).filter(CacheDadosBI.id_cache == id)
        result = await session.execute(query)
        peca_ordem_servico = result.scalar_one_or_none()
        
        if peca_ordem_servico:
            await session.delete(peca_ordem_servico)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Cache Dados BI não encontrado', status_code=status.HTTP_404_NOT_FOUND)
   