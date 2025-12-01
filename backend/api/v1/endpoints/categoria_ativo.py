from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session
from models.categoria_ativo_model import CategoriaAtivo
from schemas.categoria_ativo_schema import CategoriaAtivoCreate, CategoriaAtivoResponse

router = APIRouter()



@router.get('/', status_code=status.HTTP_200_OK, response_model=List[CategoriaAtivoResponse])
async def get_categorias(db: AsyncSession = Depends(get_session)):
    query = select(CategoriaAtivo)
    result = await db.execute(query)
    return result.scalars().all()



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CategoriaAtivoResponse)
async def post_categoria(ativo: CategoriaAtivoCreate, db: AsyncSession = Depends(get_session)):
    novo_ativo = CategoriaAtivo(
        **ativo.model_dump()
    )

    db.add(novo_ativo)
    await db.commit()
    await db.refresh(novo_ativo)

    return novo_ativo



@router.get('/{id}', response_model=CategoriaAtivoResponse, status_code=status.HTTP_200_OK)
async def get_categoria(id: int, db: AsyncSession = Depends(get_session)):
    query = select(CategoriaAtivo).filter(CategoriaAtivo.id == id)
    result = await db.execute(query)
    ativo = result.scalar_one_or_none()

    if ativo:
        return ativo
    else:
        raise HTTPException(status_code=404, detail='Categoria ativo não encontrada')



@router.put('/{id}', response_model=CategoriaAtivoResponse, status_code=status.HTTP_202_ACCEPTED)
async def put_categoria(id: int, categoria_ativo: CategoriaAtivoCreate, db: AsyncSession = Depends(get_session)):
    query = select(CategoriaAtivo).filter(CategoriaAtivo.id == id)
    result = await db.execute(query)
    categoria_ativo_existente = result.scalar_one_or_none()

    if not categoria_ativo_existente:
        raise HTTPException(status_code=404, detail='Categoria ativo não encontrada')

    data = categoria_ativo.model_dump()

    categoria_ativo_existente.id_organizacao = data["id_organizacao"]
    categoria_ativo_existente.codigo = data["codigo"]
    categoria_ativo_existente.nome = data["nome"]
    categoria_ativo_existente.descricao = data["descricao"]
    categoria_ativo_existente.metodo_depreciacao = data["metodo_depreciacao"]
    categoria_ativo_existente.vida_util_padrao_anos = data["vida_util_padrao_anos"]
    categoria_ativo_existente.taxa_residual_padrao = data["taxa_residual_padrao"]
    categoria_ativo_existente.nivel_hierarquia = data["nivel_hierarquia"]
    categoria_ativo_existente.caminho_string = data["caminho_string"]

    await db.commit()
    await db.refresh(categoria_ativo_existente)

    return categoria_ativo_existente



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_categoria(id: int, db: AsyncSession = Depends(get_session)):
    query = select(CategoriaAtivo).filter(CategoriaAtivo.id == id)
    result = await db.execute(query)
    ativo = result.scalar_one_or_none()

    if not ativo:
        raise HTTPException(status_code=404, detail='Categoria ativo não encontrada')

    await db.delete(ativo)
    await db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
