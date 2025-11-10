from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from uuid import UUID

class AtivoBase(BaseModel):
    id_organizacao: int
    id_categoria: int
    id_localizacao: int
    id_fornecedor: Optional[int]
    numero_tag: str
    nome: str
    modelo: Optional[str]
    fabricante: Optional[str]
    status_ativo: Optional[str] = "ativo"
    criticidade: Optional[str] = "medio"
    custo_aquisicao: Optional[float]
    valor_atual: Optional[float]
    valor_residual: Optional[float]
    especificacoes: Optional[dict]
    parametros_tecnicos: Optional[dict]

class AtivoCreate(AtivoBase):
    pass

class AtivoResponse(AtivoBase):
    id: int
    uuid: UUID
    data_criacao: datetime

    class Config:
        orm_mode = True
