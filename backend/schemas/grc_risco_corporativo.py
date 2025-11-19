from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class RiscoCorporativoBase(BaseModel):
    codigo: str
    categoria_risco_id: int
    descricao: str
    causa: Optional[str] = None
    consequencia: Optional[str] = None
    probabilidade: Optional[int] = None
    impacto: Optional[int] = None
    severidade: Optional[int] = None
    proprietario_id: int
    data_identificacao: Optional[date] = None
    status: Optional[str] = "ATIVO"


class RiscoCorporativoCreate(RiscoCorporativoBase):
    pass


class RiscoCorporativoUpdate(BaseModel):
    codigo: Optional[str] = None
    categoria_risco_id: Optional[int] = None
    descricao: Optional[str] = None
    causa: Optional[str] = None
    consequencia: Optional[str] = None
    probabilidade: Optional[int] = None
    impacto: Optional[int] = None
    severidade: Optional[int] = None
    proprietario_id: Optional[int] = None
    data_identificacao: Optional[date] = None
    status: Optional[str] = None


class RiscoCorporativoResponse(RiscoCorporativoBase):
    id: int
    criado_em: datetime
    criado_por: int

    class Config:
        from_attributes = True
