from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class AuditoriaBase(BaseModel):
    codigo: str
    tipo_auditoria: str
    escopo: str
    normativo_referencia: Optional[str] = None
    data_planejada: Optional[date] = None
    data_realizacao: Optional[date] = None
    auditor_principal_id: Optional[int] = None
    resultado: Optional[str] = None
    relatorio_path: Optional[str] = None


class AuditoriaCreate(AuditoriaBase):
    pass


class AuditoriaUpdate(BaseModel):
    codigo: Optional[str] = None
    tipo_auditoria: Optional[str] = None
    escopo: Optional[str] = None
    normativo_referencia: Optional[str] = None
    data_planejada: Optional[date] = None
    data_realizacao: Optional[date] = None
    auditor_principal_id: Optional[int] = None
    resultado: Optional[str] = None
    relatorio_path: Optional[str] = None


class AuditoriaResponse(AuditoriaBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True
