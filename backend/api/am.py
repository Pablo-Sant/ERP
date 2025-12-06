from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from core.deps import get_db
from schemas.ativo_schema import AtivoCreate, AtivoResponse, AtivoUpdate
from services.ativo_service import AtivoService

router = APIRouter(prefix="/ativos", tags=["ativos"])

@router.post("/", response_model=AtivoResponse, status_code=201)
def criar_ativo(ativo: AtivoCreate, db: Session = Depends(get_db)):
    try:
        return AtivoService.criar_ativo(db, ativo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno ao criar ativo")

@router.get("/", response_model=List[AtivoResponse])
def listar_ativos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return AtivoService.listar_ativos(db, skip, limit)

@router.get("/buscar", response_model=List[AtivoResponse])
def buscar_ativos(
    id_categoria: Optional[int] = None,
    id_localizacao: Optional[int] = None,
    status: Optional[str] = None,
    criticidade: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Validar status e criticidade
    if status and status not in ['planejado', 'ativo', 'inativo', 'em_manutencao', 'baixado', 'descartado', 'perdido']:
        raise HTTPException(status_code=400, detail="Status inválido")
    
    if criticidade and criticidade not in ['baixa', 'medio', 'alta', 'critico']:
        raise HTTPException(status_code=400, detail="Criticidade inválida")
    
    return AtivoService.buscar_ativos(
        db, id_categoria, id_localizacao, status, criticidade
    )

@router.get("/{ativo_id}", response_model=AtivoResponse)
def obter_ativo(ativo_id: int, db: Session = Depends(get_db)):
    ativo = AtivoService.obter_ativo(db, ativo_id)
    if not ativo:
        raise HTTPException(status_code=404, detail="Ativo não encontrado")
    return ativo

@router.put("/{ativo_id}", response_model=AtivoResponse)
def atualizar_ativo(
    ativo_id: int,
    ativo_update: AtivoUpdate,
    db: Session = Depends(get_db)
):
    try:
        ativo = AtivoService.atualizar_ativo(db, ativo_id, ativo_update)
        if not ativo:
            raise HTTPException(status_code=404, detail="Ativo não encontrado")
        return ativo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{ativo_id}", status_code=204)
def excluir_ativo(ativo_id: int, db: Session = Depends(get_db)):
    try:
        success = AtivoService.excluir_ativo(db, ativo_id)
        if not success:
            raise HTTPException(status_code=404, detail="Ativo não encontrado")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))