from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class AtivoBase(BaseModel):
    id_organizacao: Optional[int] = Field(default=1)
    id_categoria: int
    id_localizacao: int
    id_fornecedor: Optional[int] = None
    numero_tag: str = Field(..., max_length=100)
    numero_serie: Optional[str] = Field(None, max_length=100)
    nome: str = Field(..., max_length=255)
    modelo: Optional[str] = Field(None, max_length=255)
    fabricante: Optional[str] = Field(None, max_length=255)
    descricao: Optional[str] = None
    status_ativo: Optional[str] = Field(
        default="ativo",
        pattern="^(planejado|ativo|inativo|em_manutencao|baixado|descartado|perdido)$"
    )
    criticidade: Optional[str] = Field(
        default="medio",
        pattern="^(baixa|medio|alta|critico)$"
    )
    data_aquisicao: Optional[date] = None
    custo_aquisicao: Optional[Decimal] = None
    numero_ordem_compra: Optional[str] = Field(None, max_length=100)
    data_vencimento_garantia: Optional[date] = None
    vida_util_anos: Optional[int] = None
    valor_residual: Optional[Decimal] = Field(default=0)
    valor_atual: Optional[Decimal] = None
    depreciacao_acumulada: Optional[Decimal] = Field(default=0)
    especificacoes: Optional[dict] = None
    parametros_tecnicos: Optional[dict] = None
    observacoes: Optional[str] = None
    criado_por: Optional[int] = None

class AtivoCreate(AtivoBase):
    pass

class AtivoUpdate(BaseModel):
    id_localizacao: Optional[int] = None
    status_ativo: Optional[str] = Field(
        None,
        pattern="^(planejado|ativo|inativo|em_manutencao|baixado|descartado|perdido)$"
    )
    criticidade: Optional[str] = Field(
        None,
        pattern="^(baixa|medio|alta|critico)$"
    )
    valor_atual: Optional[Decimal] = None
    observacoes: Optional[str] = None

class AtivoResponse(AtivoBase):
    id: int
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        from_attributes = True