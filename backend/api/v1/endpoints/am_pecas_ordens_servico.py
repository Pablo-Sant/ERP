from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.am_pecas_ordem_servico import PecasOrdemServico
from schemas.peca_ordem_servico_schema import PecasOrdemServicoResponse, PecasOrdemServicoCreate

router = APIRouter()

@router.get('/', status_code = status.HTTP_200_OK, response_model=List[PecasOrdemServicoResponse])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PecasOrdemServico)
        result = await session.execute(query)
        ativos:List[PecasOrdemServico] = result.scalars().all()
        
        return ativos
    
@router.post('/{id}', status_code = status.HTTP_201_CREATED, response_model=PecasOrdemServicoResponse)
async def post_curso(id:int, ativo:PecasOrdemServicoCreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        novo_ativo = PecasOrdemServico(
            id_ordem_servico = ativo.id_ordem_servico,
            numero_peca = ativo.numero_peca,
            nome_peca = ativo.nome_peca,
            quantidade = ativo.quantidade,
            custo_unitario = ativo.custo_unitario,
            custo_total = ativo.custo_total   
        )
        
        db.add(novo_ativo)
        db.commit()
        db.refresh(novo_ativo)
        
        return novo_ativo
    

@router.get('/{id}', response_model=PecasOrdemServicoResponse, status_code=status.HTTP_200_OK)
async def get_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PecasOrdemServico).filter(PecasOrdemServico.id == id)
        result = await session.execute(query)
        ativo = result.scalar_one_or_none()
        
        if ativo:
            return ativo
        else:
            raise HTTPException(detail='Peça de ordem de serviço não encontrada', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id}', response_model=PecasOrdemServicoResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_produto(id:int, pecas_ordem_servico:PecasOrdemServicoCreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PecasOrdemServico).filter(PecasOrdemServico.id == id)
        result = await session.execute(query)
        pecas_ordem_servico = result.scalar_one_or_none()
        
        if pecas_ordem_servico:
            pecas_ordem_servico.id_ordem_servico = pecas_ordem_servico.id_ordem_servico,
            pecas_ordem_servico.numero_peca = pecas_ordem_servico.numero_peca,
            pecas_ordem_servico.nome_peca = pecas_ordem_servico.nome_peca,
            pecas_ordem_servico.quantidade = pecas_ordem_servico.quantidade,
            pecas_ordem_servico.custo_unitario = pecas_ordem_servico.custo_unitario,
            pecas_ordem_servico.custo_total = pecas_ordem_servico.custo_total 
            
            return pecas_ordem_servico
        
        else:
            raise HTTPException(detail='Peça ordem de serviço não encontrada', status_code=status.HTTP_404_NOT_FOUND)
        

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PecasOrdemServico).filter(PecasOrdemServico.id == id)
        result = await session.execute(query)
        peca_ordem_servico = result.scalar_one_or_none()
        
        if peca_ordem_servico:
            await session.delete(peca_ordem_servico)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Peça ordem de serviço não encontrada', status_code=status.HTTP_404_NOT_FOUND)
   