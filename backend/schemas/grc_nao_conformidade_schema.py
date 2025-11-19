from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class NaoConformidadeAuditoriaBase(BaseModel):
    auditoria_id: int
    descricao: str
    requisito_nao_atendido: Optional[str] = None
    classificacao: Optional[str] = None
    prazo_correcao: Optional[date] = None
    responsavel_correcao_id: Optional[int] = None
    data_correcao: Optional[date] = None
    evidencia_correcao: Optional[str] = None
    status: Optional[str] = "ABERTA"


class NaoConformidadeAuditoriaCreate(NaoConformidadeAuditoriaBase):
    pass


class NaoConformidadeAuditoriaUpdate(BaseModel):
    auditoria_id: Optional[int] = None
    descricao: Optional[str] = None
    requisito_nao_atendido: Optional[str] = None
    classificacao: Optional[str] = None
    prazo_correcao: Optional[date] = None
    responsavel_correcao_id: Optional[int] = None
    data_correcao: Optional[date] = None
    evidencia_correcao: Optional[str] = None
    status: Optional[str] = None


class NaoConformidadeAuditoriaResponse(NaoConformidadeAuditoriaBase):
    id: int

    class Config:
        from_attributes = True
