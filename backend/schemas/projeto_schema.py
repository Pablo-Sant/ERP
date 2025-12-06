from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

class ProjetoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=200)
    descricao: Optional[str] = None
    id_cliente: Optional[int] = None
    id_gerente: Optional[int] = None
    data_inicio_prevista: Optional[date] = None
    data_fim_prevista: Optional[date] = None
    orcamento_total: Optional[float] = Field(0.0, ge=0)
    status: Optional[str] = "PLANEJAMENTO"
    prioridade: Optional[str] = "MEDIA"
    porcentagem_conclusao: Optional[int] = Field(0, ge=0, le=100)

class ProjetoCreate(ProjetoBase):
    pass

class ProjetoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=200)
    descricao: Optional[str] = None
    id_cliente: Optional[int] = None
    id_gerente: Optional[int] = None
    data_inicio_prevista: Optional[date] = None
    data_fim_prevista: Optional[date] = None
    orcamento_total: Optional[float] = Field(None, ge=0)
    status: Optional[str] = None
    prioridade: Optional[str] = None
    porcentagem_conclusao: Optional[int] = Field(None, ge=0, le=100)

class ProjetoResponse(ProjetoBase):
    id_projeto: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Isso permite criar do ORM