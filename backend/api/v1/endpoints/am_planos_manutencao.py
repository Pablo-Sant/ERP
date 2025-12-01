from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.am_planos_manutencao_model import PlanosManutencao
from schemas.planos_manutencao_schema import PlanosManutencaoResponse, PlanosManutencaoCreate

router = APIRouter()

@router.get('/', status_code = status.HTTP_200_OK, response_model=List[PlanosManutencaoResponse])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PlanosManutencao)
        result = await session.execute(query)
        ativos:List[PlanosManutencao] = result.scalars().all()
        
        return ativos
    
@router.post('/{id}', status_code = status.HTTP_201_CREATED, response_model=PlanosManutencaoResponse)
async def post_curso(id:int, plano_manutencao:PlanosManutencaoCreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        novo_plano_manutencao = PlanosManutencao(
            nome = plano_manutencao.nome,
            descricao = plano_manutencao.descricao,
            tipo_manutencao = plano_manutencao.tipo_manutencao,
            tipo_frequencia = plano_manutencao.tipo_frequencia,
            valor_frequencia = plano_manutencao.valor_frequencia,
            duracao_estimada_minutos = plano_manutencao.duracao_estimada_minutos,
            custo_estimado = plano_manutencao.custo_estimado,
            procedimentos = plano_manutencao.procedimentos,
            ativo = plano_manutencao.ativo  
        )
        
        db.add(novo_plano_manutencao)
        db.commit()
        db.refresh(novo_plano_manutencao)
        
        return novo_plano_manutencao
    

@router.get('/{id}', response_model=PlanosManutencaoResponse, status_code=status.HTTP_200_OK)
async def get_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PlanosManutencao).filter(PlanosManutencao.id == id)
        result = await session.execute(query)
        ativo = result.scalar_one_or_none()
        
        if ativo:
            return ativo
        else:
            raise HTTPException(detail='Plano de manutenção não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id}', response_model=PlanosManutencaoResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_produto(id:int, planos_manutencao:PlanosManutencaoCreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PlanosManutencao).filter(PlanosManutencao.id == id)
        result = await session.execute(query)
        planos_manutencao = result.scalar_one_or_none()
        
        if planos_manutencao:
            planos_manutencao.id_ordem_servico = planos_manutencao.id_ordem_servico,
            planos_manutencao.numero_peca = planos_manutencao.numero_peca,
            planos_manutencao.nome_peca = planos_manutencao.nome_peca,
            planos_manutencao.quantidade = planos_manutencao.quantidade,
            planos_manutencao.custo_unitario = planos_manutencao.custo_unitario,
            planos_manutencao.custo_total = planos_manutencao.custo_total 
            
            return planos_manutencao
        
        else:
            raise HTTPException(detail='Plano de manutenção não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PlanosManutencao).filter(PlanosManutencao.id == id)
        result = await session.execute(query)
        peca_ordem_servico = result.scalar_one_or_none()
        
        if peca_ordem_servico:
            await session.delete(peca_ordem_servico)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Plano de manutenção não encontrado', status_code=status.HTTP_404_NOT_FOUND)
   