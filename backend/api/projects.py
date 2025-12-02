# api/projects.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, func
from core.deps import get_session, get_current_user
from models.projeto_model import ProjetoModel
from models.usuario import UsuarioModel
from schemas.projeto_schema import ProjetoCreate, ProjetoUpdate, ProjetoResponse
from typing import List, Optional

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_model=List[ProjetoResponse])
async def get_projects(
    db: AsyncSession = Depends(get_session),
    search: Optional[str] = None,
    status_filter: Optional[str] = None,
    current_user: UsuarioModel = Depends(get_current_user)
):
    query = select(ProjetoModel)
    
    if search:
        query = query.filter(
            or_(
                ProjetoModel.nome.ilike(f"%{search}%"),
                ProjetoModel.descricao.ilike(f"%{search}%"),
                ProjetoModel.cliente.ilike(f"%{search}%")
            )
        )
    
    if status_filter and status_filter != "all":
        query = query.filter(ProjetoModel.status == status_filter)
    
    query = query.order_by(ProjetoModel.data_criacao.desc())
    result = await db.execute(query)
    projetos = result.scalars().all()
    
    return projetos

@router.post("/", response_model=ProjetoResponse)
async def create_project(
    projeto: ProjetoCreate,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user)
):
    db_projeto = ProjetoModel(
        **projeto.model_dump(),
        criado_por=current_user.id
    )
    
    db.add(db_projeto)
    await db.commit()
    await db.refresh(db_projeto)
    return db_projeto

@router.get("/{project_id}", response_model=ProjetoResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user)
):
    query = select(ProjetoModel).filter(ProjetoModel.id == project_id)
    result = await db.execute(query)
    projeto = result.scalar_one_or_none()
    
    if not projeto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    return projeto

@router.put("/{project_id}", response_model=ProjetoResponse)
async def update_project(
    project_id: int,
    projeto_update: ProjetoUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user)
):
    query = select(ProjetoModel).filter(ProjetoModel.id == project_id)
    result = await db.execute(query)
    projeto = result.scalar_one_or_none()
    
    if not projeto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    update_data = projeto_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(projeto, field, value)
    
    await db.commit()
    await db.refresh(projeto)
    return projeto

@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user)
):
    query = select(ProjetoModel).filter(ProjetoModel.id == project_id)
    result = await db.execute(query)
    projeto = result.scalar_one_or_none()
    
    if not projeto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    await db.delete(projeto)
    await db.commit()
    return {"message": "Projeto deletado com sucesso"}