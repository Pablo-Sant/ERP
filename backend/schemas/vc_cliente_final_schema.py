from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from decimal import Decimal

class ClienteFinalBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100, description="Nome do cliente")
    cpf_cnpj: Optional[str] = Field(None, description="CPF ou CNPJ")  
    email: Optional[str] = Field(None, max_length=100, description="E-mail do cliente")
    telefone: Optional[str] = Field(None, max_length=20, description="Telefone do cliente")
    endereco: Optional[str] = Field(None, max_length=200, description="Endereço completo")
    cidade: Optional[str] = Field(None, max_length=100, description="Cidade")


class ClienteFinalCreate(ClienteFinalBase):
    pass

class ClienteFinalUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    cpf_cnpj: Optional[str] = Field(None) 
    email: Optional[str] = Field(None, max_length=100)
    telefone: Optional[str] = Field(None, max_length=20)
    endereco: Optional[str] = Field(None, max_length=200)
    cidade: Optional[str] = Field(None, max_length=100)
    data_ultima_compra: Optional[date] = Field(None)
    valor_compra: Optional[Decimal] = Field(None, ge=0)

class ClienteFinalResponse(ClienteFinalBase):
    cliente_finalid: int = Field(..., description="ID do cliente")
    data_ultima_compra: date = Field(..., description="Data da última compra")
    valor_compra: Decimal = Field(..., ge=0, description="Valor da última compra")
    
    class Config:
        from_attributes = True