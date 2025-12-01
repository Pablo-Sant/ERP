from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.bi_metrica_kpi_model import MetricaKPI
from schemas.bi_metrica_kpi_schema import MetricaKPICreate, MetricaKPIRead

router = APIRouter()

@router.get('/', status_code = status.HTTP_200_OK, response_model=List[MetricaKPIRead])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MetricaKPI)
        result = await session.execute(query)
        ativos:List[MetricaKPI] = result.scalars().all()
        
        return ativos
    
    
@router.post('/', status_code = status.HTTP_201_CREATED, response_model=MetricaKPIRead)
async def post_curso(plano_manutencao:MetricaKPICreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        novo_plano_manutencao = MetricaKPI(
            nome = plano_manutencao.nome,
            descricao = plano_manutencao.descricao,
            formula_calculo = plano_manutencao.formula_calculo,
            unidade_medida = plano_manutencao.unidade_medida,
            categoria = plano_manutencao.categoria  
        )
        
        db.add(novo_plano_manutencao)
        db.commit()
        db.refresh(novo_plano_manutencao)
        
        return novo_plano_manutencao
    

@router.get('/{id}', response_model=MetricaKPIRead, status_code=status.HTTP_200_OK)
async def get_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MetricaKPI).filter(MetricaKPI.id_metrica == id)
        result = await session.execute(query)
        ativo = result.scalar_one_or_none()
        
        if ativo:
            return ativo
        else:
            raise HTTPException(detail='Métrica KPI não encontrada', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id}', response_model=MetricaKPIRead, status_code=status.HTTP_202_ACCEPTED)
async def put_produto(id:int, plano_manutencao:MetricaKPICreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MetricaKPI).filter(MetricaKPI.id_metrica == id)
        result = await session.execute(query)
        registro_calibracao = result.scalar_one_or_none()
        
        if registro_calibracao:
            registro_calibracao.nome = plano_manutencao.nome,
            registro_calibracao.descricao = plano_manutencao.descricao,
            registro_calibracao.formula_calculo = plano_manutencao.formula_calculo,
            registro_calibracao.unidade_medida = plano_manutencao.unidade_medida,
            registro_calibracao.categoria = plano_manutencao.categoria  
            
            return registro_calibracao
        
        else:
            raise HTTPException(detail='Métrica KPI não encontrada', status_code=status.HTTP_404_NOT_FOUND)
        

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MetricaKPI).filter(MetricaKPI.id_metrica == id)
        result = await session.execute(query)
        peca_ordem_servico = result.scalar_one_or_none()
        
        if peca_ordem_servico:
            await session.delete(peca_ordem_servico)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Métrica KPI não encontrado', status_code=status.HTTP_404_NOT_FOUND)
   