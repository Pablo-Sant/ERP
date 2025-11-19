from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

class ClienteFinalBase(BaseModel):
    nome: str
    cpf_cnpj: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    data_ultima_compra: Optional[date] = None
    valor_compra: Optional[Decimal] = None


class ClienteFinalCreate(ClienteFinalBase):
    pass


class ClienteFinalRead(ClienteFinalBase):
    cliente_finalid: int

    class Config:
        orm_mode = True