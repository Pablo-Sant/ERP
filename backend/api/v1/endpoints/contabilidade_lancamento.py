from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session

from models.contabilidade_lancamento import ContabilidadeLancamentos
from schemas.contabilidade_lancamentos_contabeis import ContabilidadeLancamentosCreate, ContabilidadeLancamentosResponse

router = APIRouter()



@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ContabilidadeLancamentosResponse])
async def get_categorias(db: AsyncSession = Depends(get_session)):
    query = select(ContabilidadeLancamentos)
    result = await db.execute(query)
    return result.scalars().all()



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ContabilidadeLancamentosResponse)
async def post_categoria(ativo: ContabilidadeLancamentosCreate, db: AsyncSession = Depends(get_session)):
    novo_ativo = ContabilidadeLancamentos(
        **ativo.model_dump()
    )

    db.add(novo_ativo)
    await db.commit()
    await db.refresh(novo_ativo)

    return novo_ativo



@router.get('/{id}', response_model=ContabilidadeLancamentosResponse, status_code=status.HTTP_200_OK)
async def get_categoria(id: int, db: AsyncSession = Depends(get_session)):
    query = select(ContabilidadeLancamentos).filter(ContabilidadeLancamentos.id_lancamento == id)
    result = await db.execute(query)
    ativo = result.scalar_one_or_none()

    if ativo:
        return ativo
    else:
        raise HTTPException(status_code=404, detail='Lançamento não encontrado')



@router.put('/{id}', response_model=ContabilidadeLancamentosResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_categoria(id: int, categoria_ativo: ContabilidadeLancamentosCreate, db: AsyncSession = Depends(get_session)):
    query = select(ContabilidadeLancamentos).filter(ContabilidadeLancamentos.id_lancamento == id)
    result = await db.execute(query)
    categoria_ativo_existente = result.scalar_one_or_none()

    if not categoria_ativo_existente:
        raise HTTPException(status_code=404, detail='Lançamento não encontrado')

    data = categoria_ativo.model_dump()

    categoria_ativo_existente.data = data["data"]
    categoria_ativo_existente.historico = data["historico"]
    categoria_ativo_existente.valor = data["valor"]
    categoria_ativo_existente.debito_conta_id = data["debito_conta_id"]
    categoria_ativo_existente.credito_conta_id = data["credito_conta_id"]
    categoria_ativo_existente.origem_modulo = data["origem_modulo"]
    categoria_ativo_existente.origem_id = data["origem_id"]

    await db.commit()
    await db.refresh(categoria_ativo_existente)

    return categoria_ativo_existente



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_categoria(id: int, db: AsyncSession = Depends(get_session)):
    query = select(ContabilidadeLancamentos).filter(ContabilidadeLancamentos.id_lancamento == id)
    result = await db.execute(query)
    ativo = result.scalar_one_or_none()

    if not ativo:
        raise HTTPException(status_code=404, detail='Lançamento não encontrado')

    await db.delete(ativo)
    await db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
