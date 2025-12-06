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


class ClienteFinalResponse(ClienteFinalBase):
    cliente_finalid: int

    class Config:
        from_attributes = True  # Corrigido: de orm_mode para from_attributes


# ADICIONE ESTA CLASSE
class ClienteFinalUpdate(BaseModel):
    """Schema para atualização parcial de cliente final"""
    nome: Optional[str] = None
    cpf_cnpj: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    data_ultima_compra: Optional[date] = None
    valor_compra: Optional[Decimal] = None
    
    class Config:
        from_attributes = True