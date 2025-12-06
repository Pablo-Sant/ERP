from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from typing import List, Optional

from core.deps import get_session, get_current_user
from models.projeto_model import ProjetoModel
from models.usuario import UsuarioModel
from schemas.projeto_schema import ProjetoCreate, ProjetoUpdate, ProjetoResponse

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_model=List[ProjetoResponse])
async def get_projects(
    db: AsyncSession = Depends(get_session),
    search: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Lista todos os projetos
    """
    try:
        query = select(ProjetoModel)
        
        if search:
            query = query.filter(
                or_(
                    ProjetoModel.nome.ilike(f"%{search}%"),
                    ProjetoModel.descricao.ilike(f"%{search}%"),
                )
            )
        
        if status_filter and status_filter.lower() != "all":
            query = query.filter(ProjetoModel.status == status_filter.upper())
        
        query = query.order_by(ProjetoModel.created_at.desc())
        result = await db.execute(query)
        projetos = result.scalars().all()
        
        return projetos
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

@router.post("/", response_model=ProjetoResponse)
async def create_project(
    projeto: ProjetoCreate,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Cria um novo projeto
    """
    try:
        # Converte para dict e adiciona id_gerente se não fornecido
        projeto_data = projeto.model_dump()
        
        if projeto_data.get('id_gerente') is None:
            projeto_data['id_gerente'] = current_user.id
        
        db_projeto = ProjetoModel(**projeto_data)
        
        db.add(db_projeto)
        await db.commit()
        await db.refresh(db_projeto)
        
        return db_projeto
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar projeto: {str(e)}"
        )

@router.get("/{project_id}", response_model=ProjetoResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Obtém um projeto por ID
    """
    query = select(ProjetoModel).filter(ProjetoModel.id_projeto == project_id)
    result = await db.execute(query)
    projeto = result.scalar_one_or_none()
    
    if not projeto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projeto com ID {project_id} não encontrado"
        )
    
    return projeto