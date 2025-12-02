# schemas/ps_projeto_schema.py
from pydantic import BaseModel, validator, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

# Enums para status e prioridade
class StatusProjeto(str, Enum):
    PLANEJAMENTO = "PLANEJAMENTO"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    PAUSADO = "PAUSADO"
    CONCLUIDO = "CONCLUIDO"
    CANCELADO = "CANCELADO"

class PrioridadeProjeto(str, Enum):
    BAIXA = "BAIXA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    URGENTE = "URGENTE"

# Schema base
class ProjetoBase(BaseModel):
    nome: str = Field(..., max_length=200, description="Nome do projeto")
    descricao: Optional[str] = Field(None, description="Descrição detalhada do projeto")
    id_gerente: Optional[int] = Field(None, description="ID do gerente responsável")
    id_cliente: Optional[int] = Field(None, description="ID do cliente")
    data_inicio_prevista: Optional[date] = Field(None, description="Data de início prevista")
    data_fim_prevista: Optional[date] = Field(None, description="Data de término prevista")
    data_inicio_real: Optional[date] = Field(None, description="Data de início real")
    data_fim_real: Optional[date] = Field(None, description="Data de término real")
    orcamento_total: Optional[float] = Field(0.0, ge=0, description="Orçamento total do projeto")
    custo_real: Optional[float] = Field(0.0, ge=0, description="Custo real do projeto")
    status: StatusProjeto = Field(StatusProjeto.PLANEJAMENTO, description="Status do projeto")
    prioridade: PrioridadeProjeto = Field(PrioridadeProjeto.MEDIA, description="Prioridade do projeto")
    porcentagem_conclusao: Optional[int] = Field(0, ge=0, le=100, description="Porcentagem de conclusão (0-100)")

    @validator('orcamento_total', 'custo_real', pre=True)
    def validate_currency(cls, v):
        if v is not None:
            return round(float(v), 2)
        return v

# Schema para criação
class ProjetoCreate(ProjetoBase):
    pass

# Schema para atualização
class ProjetoUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=200)
    descricao: Optional[str] = None
    id_gerente: Optional[int] = None
    id_cliente: Optional[int] = None
    data_inicio_prevista: Optional[date] = None
    data_fim_prevista: Optional[date] = None
    data_inicio_real: Optional[date] = None
    data_fim_real: Optional[date] = None
    orcamento_total: Optional[float] = Field(None, ge=0)
    custo_real: Optional[float] = Field(None, ge=0)
    status: Optional[StatusProjeto] = None
    prioridade: Optional[PrioridadeProjeto] = None
    porcentagem_conclusao: Optional[int] = Field(None, ge=0, le=100)

# Schema para resposta (leitura)
class ProjetoResponse(ProjetoBase):
    id_projeto: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }

# Schema com informações relacionadas (para listagem)
class ProjetoListResponse(BaseModel):
    id_projeto: int
    nome: str
    descricao: Optional[str]
    status: StatusProjeto
    prioridade: PrioridadeProjeto
    porcentagem_conclusao: int
    data_inicio_prevista: Optional[date]
    data_fim_prevista: Optional[date]
    orcamento_total: float
    custo_real: float
    cliente_nome: Optional[str] = None  # Nome do cliente (join)
    gerente_nome: Optional[str] = None  # Nome do gerente (join)
    created_at: datetime

    class Config:
        from_attributes = True