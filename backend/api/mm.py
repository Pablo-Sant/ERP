# api/mm_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, func
from typing import List, Optional
from datetime import datetime

from core.database import get_db
from models.mm_produto_model import Produto
from models.mm_empresas_model import Empresa
from models.mm_categorias_model import Categoria
from models.mm_armazens_model import Armazem
from schemas.mm_produto_schema import (
    ProdutoCreate, ProdutoUpdate, ProdutoResponse
)
from schemas.mm_empresas_schema import (
    EmpresaCreate, EmpresaUpdate, EmpresaResponse
)
from schemas.mm_categorias_schema import (
    CategoriaCreate, CategoriaUpdate, CategoriaResponse
)
from schemas.mm_armazem_schema import (
    ArmazemCreate, ArmazemUpdate, ArmazemResponse
)
from api.auth import get_current_user
from models.usuario import UsuarioModel

router = APIRouter(prefix="/mm", tags=["Material Management"])

# ========== PRODUTOS ==========

@router.get("/produtos", response_model=List[ProdutoResponse])
async def listar_produtos(
    db: AsyncSession = Depends(get_db),
    empresa_id: Optional[int] = Query(None),
    categoria_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista todos os produtos"""
    query = select(Produto)
    
    if empresa_id:
        query = query.where(Produto.empresa_id == empresa_id)
    if categoria_id:
        query = query.where(Produto.categoria_id == categoria_id)
    if search:
        query = query.where(
            or_(
                Produto.nome.ilike(f"%{search}%"),
                Produto.descricao.ilike(f"%{search}%") if Produto.descricao else False
            )
        )
    
    query = query.offset(skip).limit(limit).order_by(Produto.nome)
    
    result = await db.execute(query)
    produtos = result.scalars().all()
    return produtos

@router.get("/produtos/{produto_id}", response_model=ProdutoResponse)
async def get_produto(
    produto_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Obtém um produto específico"""
    query = select(Produto).where(Produto.id == produto_id)
    result = await db.execute(query)
    produto = result.scalar_one_or_none()
    
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    return produto

@router.post("/produtos", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
async def criar_produto(
    produto: ProdutoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria um novo produto"""
    try:
        # Verificar se empresa existe
        empresa_query = select(Empresa).where(Empresa.id == produto.empresa_id)
        empresa_result = await db.execute(empresa_query)
        if not empresa_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empresa não encontrada"
            )
        
        # Verificar se categoria existe
        categoria_query = select(Categoria).where(Categoria.id == produto.categoria_id)
        categoria_result = await db.execute(categoria_query)
        if not categoria_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Categoria não encontrada"
            )
        
        db_produto = Produto(**produto.dict())
        db.add(db_produto)
        await db.commit()
        await db.refresh(db_produto)
        return db_produto
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar produto: {str(e)}"
        )

@router.put("/produtos/{produto_id}", response_model=ProdutoResponse)
async def atualizar_produto(
    produto_id: int,
    produto_update: ProdutoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Atualiza um produto existente"""
    query = select(Produto).where(Produto.id == produto_id)
    result = await db.execute(query)
    db_produto = result.scalar_one_or_none()
    
    if not db_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    update_data = produto_update.dict(exclude_unset=True)
    
    # Verificar se empresa existe se for atualizar
    if 'empresa_id' in update_data:
        empresa_query = select(Empresa).where(Empresa.id == update_data['empresa_id'])
        empresa_result = await db.execute(empresa_query)
        if not empresa_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empresa não encontrada"
            )
    
    # Verificar se categoria existe se for atualizar
    if 'categoria_id' in update_data:
        categoria_query = select(Categoria).where(Categoria.id == update_data['categoria_id'])
        categoria_result = await db.execute(categoria_query)
        if not categoria_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Categoria não encontrada"
            )
    
    for field, value in update_data.items():
        setattr(db_produto, field, value)
    
    db_produto.data_atualizacao = datetime.now()
    
    try:
        await db.commit()
        await db.refresh(db_produto)
        return db_produto
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar produto: {str(e)}"
        )

@router.delete("/produtos/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_produto(
    produto_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Exclui um produto"""
    query = select(Produto).where(Produto.id == produto_id)
    result = await db.execute(query)
    produto = result.scalar_one_or_none()
    
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    try:
        await db.delete(produto)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir produto: {str(e)}"
        )

# ========== EMPRESAS ==========

@router.get("/empresas", response_model=List[EmpresaResponse])
async def listar_empresas(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista todas as empresas"""
    query = select(Empresa).offset(skip).limit(limit).order_by(Empresa.nome)
    result = await db.execute(query)
    empresas = result.scalars().all()
    return empresas

@router.get("/empresas/{empresa_id}", response_model=EmpresaResponse)
async def get_empresa(
    empresa_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Obtém uma empresa específica"""
    query = select(Empresa).where(Empresa.id == empresa_id)
    result = await db.execute(query)
    empresa = result.scalar_one_or_none()
    
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    
    return empresa

@router.post("/empresas", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED)
async def criar_empresa(
    empresa: EmpresaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria uma nova empresa"""
    try:
        # Verificar se CPF/CNPJ já existe
        if empresa.cpf_cnpj:
            query = select(Empresa).where(Empresa.cpf_cnpj == empresa.cpf_cnpj)
            result = await db.execute(query)
            if result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CPF/CNPJ já cadastrado"
                )
        
        db_empresa = Empresa(**empresa.dict())
        db.add(db_empresa)
        await db.commit()
        await db.refresh(db_empresa)
        return db_empresa
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar empresa: {str(e)}"
        )

@router.put("/empresas/{empresa_id}", response_model=EmpresaResponse)
async def atualizar_empresa(
    empresa_id: int,
    empresa_update: EmpresaUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Atualiza uma empresa existente"""
    query = select(Empresa).where(Empresa.id == empresa_id)
    result = await db.execute(query)
    db_empresa = result.scalar_one_or_none()
    
    if not db_empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    
    update_data = empresa_update.dict(exclude_unset=True)
    
    # Verificar duplicidade de CPF/CNPJ
    if 'cpf_cnpj' in update_data and update_data['cpf_cnpj']:
        query = select(Empresa).where(
            Empresa.cpf_cnpj == update_data['cpf_cnpj'],
            Empresa.id != empresa_id
        )
        result = await db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF/CNPJ já cadastrado para outra empresa"
            )
    
    for field, value in update_data.items():
        setattr(db_empresa, field, value)
    
    try:
        await db.commit()
        await db.refresh(db_empresa)
        return db_empresa
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar empresa: {str(e)}"
        )

@router.delete("/empresas/{empresa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_empresa(
    empresa_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Exclui uma empresa"""
    query = select(Empresa).where(Empresa.id == empresa_id)
    result = await db.execute(query)
    empresa = result.scalar_one_or_none()
    
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    
    # Verificar se há produtos associados
    produtos_query = select(Produto).where(Produto.empresa_id == empresa_id)
    produtos_result = await db.execute(produtos_query)
    if produtos_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível excluir empresa com produtos associados"
        )
    
    try:
        await db.delete(empresa)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir empresa: {str(e)}"
        )

# ========== CATEGORIAS ==========

@router.get("/categorias", response_model=List[CategoriaResponse])
async def listar_categorias(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista todas as categorias"""
    query = select(Categoria).offset(skip).limit(limit).order_by(Categoria.nome)
    result = await db.execute(query)
    categorias = result.scalars().all()
    return categorias

@router.get("/categorias/{categoria_id}", response_model=CategoriaResponse)
async def get_categoria(
    categoria_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Obtém uma categoria específica"""
    query = select(Categoria).where(Categoria.id == categoria_id)
    result = await db.execute(query)
    categoria = result.scalar_one_or_none()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )
    
    return categoria

@router.post("/categorias", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
async def criar_categoria(
    categoria: CategoriaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria uma nova categoria"""
    try:
        # Verificar se categoria pai existe
        if categoria.categoria_pai_id:
            query = select(Categoria).where(Categoria.id == categoria.categoria_pai_id)
            result = await db.execute(query)
            if not result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Categoria pai não encontrada"
                )
        
        db_categoria = Categoria(**categoria.dict())
        db.add(db_categoria)
        await db.commit()
        await db.refresh(db_categoria)
        return db_categoria
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar categoria: {str(e)}"
        )

@router.put("/categorias/{categoria_id}", response_model=CategoriaResponse)
async def atualizar_categoria(
    categoria_id: int,
    categoria_update: CategoriaUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Atualiza uma categoria existente"""
    query = select(Categoria).where(Categoria.id == categoria_id)
    result = await db.execute(query)
    db_categoria = result.scalar_one_or_none()
    
    if not db_categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )
    
    update_data = categoria_update.dict(exclude_unset=True)
    
    # Verificar se não está tentando se tornar pai de si mesmo
    if 'categoria_pai_id' in update_data and update_data['categoria_pai_id'] == categoria_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Categoria não pode ser pai de si mesma"
        )
    
    # Verificar se categoria pai existe
    if 'categoria_pai_id' in update_data and update_data['categoria_pai_id']:
        query = select(Categoria).where(Categoria.id == update_data['categoria_pai_id'])
        result = await db.execute(query)
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Categoria pai não encontrada"
            )
    
    for field, value in update_data.items():
        setattr(db_categoria, field, value)
    
    try:
        await db.commit()
        await db.refresh(db_categoria)
        return db_categoria
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar categoria: {str(e)}"
        )

@router.delete("/categorias/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_categoria(
    categoria_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Exclui uma categoria"""
    query = select(Categoria).where(Categoria.id == categoria_id)
    result = await db.execute(query)
    categoria = result.scalar_one_or_none()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )
    
    # Verificar se há subcategorias
    query = select(Categoria).where(Categoria.categoria_pai_id == categoria_id)
    result = await db.execute(query)
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível excluir categoria com subcategorias"
        )
    
    # Verificar se há produtos associados
    produtos_query = select(Produto).where(Produto.categoria_id == categoria_id)
    produtos_result = await db.execute(produtos_query)
    if produtos_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível excluir categoria com produtos associados"
        )
    
    try:
        await db.delete(categoria)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir categoria: {str(e)}"
        )

# ========== ARMAZÉNS ==========

@router.get("/armazens", response_model=List[ArmazemResponse])
async def listar_armazens(
    db: AsyncSession = Depends(get_db),
    empresa_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Lista todos os armazéns"""
    query = select(Armazem)
    
    if empresa_id:
        query = query.where(Armazem.empresa_id == empresa_id)
    if search:
        query = query.where(
            or_(
                Armazem.nome.ilike(f"%{search}%"),
                Armazem.endereco.ilike(f"%{search}%") if Armazem.endereco else False
            )
        )
    
    query = query.offset(skip).limit(limit).order_by(Armazem.nome)
    
    result = await db.execute(query)
    armazens = result.scalars().all()
    return armazens

@router.get("/armazens/{armazem_id}", response_model=ArmazemResponse)
async def get_armazem(
    armazem_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Obtém um armazém específico"""
    query = select(Armazem).where(Armazem.id == armazem_id)
    result = await db.execute(query)
    armazem = result.scalar_one_or_none()
    
    if not armazem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Armazém não encontrado"
        )
    
    return armazem

@router.post("/armazens", response_model=ArmazemResponse, status_code=status.HTTP_201_CREATED)
async def criar_armazem(
    armazem: ArmazemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Cria um novo armazém"""
    try:
        # Verificar se empresa existe
        query = select(Empresa).where(Empresa.id == armazem.empresa_id)
        result = await db.execute(query)
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empresa não encontrada"
            )
        
        db_armazem = Armazem(**armazem.dict())
        db.add(db_armazem)
        await db.commit()
        await db.refresh(db_armazem)
        return db_armazem
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar armazém: {str(e)}"
        )

@router.put("/armazens/{armazem_id}", response_model=ArmazemResponse)
async def atualizar_armazem(
    armazem_id: int,
    armazem_update: ArmazemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Atualiza um armazém existente"""
    query = select(Armazem).where(Armazem.id == armazem_id)
    result = await db.execute(query)
    db_armazem = result.scalar_one_or_none()
    
    if not db_armazem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Armazém não encontrado"
        )
    
    update_data = armazem_update.dict(exclude_unset=True)
    
    # Verificar se empresa existe se for atualizar
    if 'empresa_id' in update_data:
        query = select(Empresa).where(Empresa.id == update_data['empresa_id'])
        result = await db.execute(query)
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empresa não encontrada"
            )
    
    for field, value in update_data.items():
        setattr(db_armazem, field, value)
    
    try:
        await db.commit()
        await db.refresh(db_armazem)
        return db_armazem
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar armazém: {str(e)}"
        )

@router.delete("/armazens/{armazem_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_armazem(
    armazem_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Exclui um armazém"""
    query = select(Armazem).where(Armazem.id == armazem_id)
    result = await db.execute(query)
    armazem = result.scalar_one_or_none()
    
    if not armazem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Armazém não encontrado"
        )
    
    try:
        await db.delete(armazem)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir armazém: {str(e)}"
        )

# ========== DASHBOARD MM ==========

@router.get("/dashboard")
async def mm_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user)
):
    """Dashboard do módulo de Materiais"""
    try:
        # Total de produtos
        produtos_query = select(func.count()).select_from(Produto)
        produtos_result = await db.execute(produtos_query)
        total_produtos = produtos_result.scalar() or 0
        
        # Total de empresas
        empresas_query = select(func.count()).select_from(Empresa)
        empresas_result = await db.execute(empresas_query)
        total_empresas = empresas_result.scalar() or 0
        
        # Total de categorias
        categorias_query = select(func.count()).select_from(Categoria)
        categorias_result = await db.execute(categorias_query)
        total_categorias = categorias_result.scalar() or 0
        
        # Total de armazéns
        armazens_query = select(func.count()).select_from(Armazem)
        armazens_result = await db.execute(armazens_query)
        total_armazens = armazens_result.scalar() or 0
        
        # Produtos sem empresa
        produtos_sem_empresa = select(func.count()).select_from(Produto).where(Produto.empresa_id.is_(None))
        sem_empresa_result = await db.execute(produtos_sem_empresa)
        total_sem_empresa = sem_empresa_result.scalar() or 0
        
        # Produtos sem categoria
        produtos_sem_categoria = select(func.count()).select_from(Produto).where(Produto.categoria_id.is_(None))
        sem_categoria_result = await db.execute(produtos_sem_categoria)
        total_sem_categoria = sem_categoria_result.scalar() or 0
        
        # Últimos produtos criados
        ultimos_produtos_query = select(Produto).order_by(Produto.data_criacao.desc()).limit(5)
        ultimos_produtos_result = await db.execute(ultimos_produtos_query)
        ultimos_produtos = ultimos_produtos_result.scalars().all()
        
        return {
            "status": "ativo",
            "modulo": "Material Management (MM)",
            "estatisticas": {
                "total_produtos": total_produtos,
                "total_empresas": total_empresas,
                "total_categorias": total_categorias,
                "total_armazens": total_armazens,
                "produtos_sem_empresa": total_sem_empresa,
                "produtos_sem_categoria": total_sem_categoria
            },
            "ultimos_produtos": [
                {
                    "id": p.id,
                    "nome": p.nome,
                    "empresa_id": p.empresa_id,
                    "categoria_id": p.categoria_id,
                    "data_criacao": p.data_criacao.isoformat() if p.data_criacao else None
                }
                for p in ultimos_produtos
            ],
            "endpoints": {
                "produtos": "/api/mm/produtos",
                "empresas": "/api/mm/empresas",
                "categorias": "/api/mm/categorias",
                "armazens": "/api/mm/armazens"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar dashboard: {str(e)}"
        )

# ========== HEALTH CHECK ==========

@router.get("/health")
async def health_check():
    """Verifica se o módulo MM está funcionando"""
    return {
        "status": "healthy",
        "module": "Material Management",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/api/mm/produtos",
            "/api/mm/empresas", 
            "/api/mm/categorias",
            "/api/mm/armazens",
            "/api/mm/dashboard"
        ]
    }