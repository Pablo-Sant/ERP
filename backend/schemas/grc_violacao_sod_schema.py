from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class ViolacaoSoDBase(BaseModel):
    usuario_id: int
    funcao_conflitante_1: Optional[str] = None
    funcao_conflitante_2: Optional[str] = None
    data_deteccao: Optional[date] = None
    status: Optional[str] = "PENDENTE"


class ViolacaoSoDCreate(ViolacaoSoDBase):
    pass


class ViolacaoSoDUpdate(BaseModel):
    usuario_id: Optional[int] = None
    funcao_conflitante_1: Optional[str] = None
    funcao_conflitante_2: Optional[str] = None
    data_deteccao: Optional[date] = None
    status: Optional[str] = None


class ViolacaoSoDResponse(ViolacaoSoDBase):
    id: int

    class Config:
        from_attributes = True
