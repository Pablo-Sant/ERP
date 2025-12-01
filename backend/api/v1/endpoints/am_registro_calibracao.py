from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.am_registro_calibracao import RegistrosCalibracao
from schemas.resgistro_calibracao_schema import RegistrosCalibracaoCreate, RegistrosCalibracaoResponse

router = APIRouter()

@router.get('/', status_code = status.HTTP_200_OK, response_model=List[RegistrosCalibracaoResponse])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RegistrosCalibracao)
        result = await session.execute(query)
        ativos:List[RegistrosCalibracao] = result.scalars().all()
        
        return ativos
    
    
@router.post('/{id}', status_code = status.HTTP_201_CREATED, response_model=RegistrosCalibracaoResponse)
async def post_curso(id:int, plano_manutencao:RegistrosCalibracaoCreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        novo_plano_manutencao = RegistrosCalibracao(
            id_ativo = plano_manutencao.id_ativo,
            data_calibracao = plano_manutencao.data_calibracao,
            data_proxima_calibracao = plano_manutencao.data_proxima_calibracao,
            calibrado_por = plano_manutencao.calibrado_por,
            numero_certificado = plano_manutencao.numero_certificado,
            padrao_utilizado = plano_manutencao.padrao_utilizado,
            condicao_encontrada = plano_manutencao.condicao_encontrada,
            condicao_final = plano_manutencao.condicao_final,
            incerteza = plano_manutencao.incerteza,
            calibracao_aprovada = plano_manutencao.calibracao_aprovada,
            observacoes = plano_manutencao.observacoes  
        )
        
        db.add(novo_plano_manutencao)
        db.commit()
        db.refresh(novo_plano_manutencao)
        
        return novo_plano_manutencao
    

@router.get('/{id}', response_model=RegistrosCalibracaoResponse, status_code=status.HTTP_200_OK)
async def get_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RegistrosCalibracao).filter(RegistrosCalibracao.id == id)
        result = await session.execute(query)
        ativo = result.scalar_one_or_none()
        
        if ativo:
            return ativo
        else:
            raise HTTPException(detail='Registro de calibração não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id}', response_model=RegistrosCalibracaoResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_produto(id:int, registro_calibracao:RegistrosCalibracaoCreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RegistrosCalibracao).filter(RegistrosCalibracao.id == id)
        result = await session.execute(query)
        registro_calibracao = result.scalar_one_or_none()
        
        if registro_calibracao:
            registro_calibracao.id_ativo = registro_calibracao.id_ativo,
            registro_calibracao.data_calibracao = registro_calibracao.data_calibracao,
            registro_calibracao.data_proxima_calibracao = registro_calibracao.data_proxima_calibracao,
            registro_calibracao.calibrado_por = registro_calibracao.calibrado_por,
            registro_calibracao.numero_certificado = registro_calibracao.numero_certificado,
            registro_calibracao.padrao_utilizado = registro_calibracao.padrao_utilizado,
            registro_calibracao.condicao_encontrada = registro_calibracao.condicao_encontrada,
            registro_calibracao.condicao_final = registro_calibracao.condicao_final,
            registro_calibracao.incerteza = registro_calibracao.incerteza,
            registro_calibracao.calibracao_aprovada = registro_calibracao.calibracao_aprovada,
            registro_calibracao.observacoes = registro_calibracao.observacoes 
            
            return registro_calibracao
        
        else:
            raise HTTPException(detail='Plano de manutenção não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_produto(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RegistrosCalibracao).filter(RegistrosCalibracao).id == id)
        result = await session.execute(query)
        peca_ordem_servico = result.scalar_one_or_none()
        
        if peca_ordem_servico:
            await session.delete(peca_ordem_servico)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Registro de manutenção não encontrado', status_code=status.HTTP_404_NOT_FOUND)
   