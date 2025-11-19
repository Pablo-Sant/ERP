from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class RequisitoNormativoBase(BaseModel):
    norma: str
    versao: Optional[str] = None
    item_norma: Optional[str] = None
    descricao_requisito: str
    data_publicacao: Optional[date] = None
    data_validade: Optional[date] = None
    responsavel_conformidade_id: Optional[int] = None
    status_conformidade: Optional[str] = "NAO_AVALIADO"


class RequisitoNormativoCreate(RequisitoNormativoBase):
    pass


class RequisitoNormativoUpdate(BaseModel):
    norma: Optional[str] = None
    versao: Optional[str] = None
    item_norma: Optional[str] = None
    descricao_requisito: Optional[str] = None
    data_publicacao: Optional[date] = None
    data_validade: Optional[date] = None
    responsavel_conformidade_id: Optional[int] = None
    status_conformidade: Optional[str] = None


class RequisitoNormativoResponse(RequisitoNormativoBase):
    id: int

    class Config:
        from_attributes = True
