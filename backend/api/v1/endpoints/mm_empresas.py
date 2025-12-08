# api/v1/endpoints/empresa.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session
from schemas.mm_empresas_schema import EmpresaCreate, EmpresaResponse, EmpresaUpdate
from services.mm_empresas_services import EmpresaService

router = APIRouter()

@router.post("/", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED)
async def criar_empresa(
    empresa: EmpresaCreate,
    db: AsyncSession = Depends(get_session)
):
    try:
        nova_empresa = await EmpresaService.criar(empresa, db)
        return nova_empresa
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=list[EmpresaResponse])
async def listar_empresas(
    db: AsyncSession = Depends(get_session)
):
    empresas = await EmpresaService.get_all(db)
    return empresas

@router.get("/{empresa_id}", response_model=EmpresaResponse)
async def buscar_empresa(
    empresa_id: int,
    db: AsyncSession = Depends(get_session)
):
    empresa = await EmpresaService.get_by_id(empresa_id, db)
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empresa com ID {empresa_id} não encontrada"
        )
    return empresa

@router.put("/{empresa_id}", response_model=EmpresaResponse)
async def atualizar_empresa(
    empresa_id: int,
    empresa_update: EmpresaUpdate,
    db: AsyncSession = Depends(get_session)
):
    try:
        empresa_atualizada = await EmpresaService.update(
            empresa_id, empresa_update, db
        )
        if not empresa_atualizada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empresa com ID {empresa_id} não encontrada"
            )
        return empresa_atualizada
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{empresa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_empresa(
    empresa_id: int,
    db: AsyncSession = Depends(get_session)
):
    try:
        sucesso = await EmpresaService.delete(empresa_id, db)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empresa com ID {empresa_id} não encontrada"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )