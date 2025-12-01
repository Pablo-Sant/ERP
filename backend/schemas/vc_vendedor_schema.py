from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

class VendedorBase(BaseModel):
    nome: str
    cpf_cnpj: str
    inscricao_estadual: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    site: Optional[str] = None
    status: Optional[str] = None
    data_cadastro: Optional[date] = None


class VendedorCreate(VendedorBase):
    pass


class VendedorResponse(VendedorBase):
    vendedorid: int

    class Config:
        orm_mode = True