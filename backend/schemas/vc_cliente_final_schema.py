# schemas/cliente_final_schema.py
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from decimal import Decimal

class ClienteFinalBase(BaseModel):
    """Schema base para cliente final - SEM validação de CPF/CNPJ aqui"""
    nome: str = Field(..., min_length=2, max_length=100, description="Nome do cliente")
    cpf_cnpj: Optional[str] = Field(None, description="CPF ou CNPJ")  # SEM min_length/max_length
    email: Optional[str] = Field(None, max_length=100, description="E-mail do cliente")
    telefone: Optional[str] = Field(None, max_length=20, description="Telefone do cliente")
    endereco: Optional[str] = Field(None, max_length=200, description="Endereço completo")
    cidade: Optional[str] = Field(None, max_length=100, description="Cidade")
    data_ultima_compra: Optional[date] = Field(None, description="Data da última compra")
    valor_compra: Optional[Decimal] = Field(None, ge=0, description="Valor da última compra")

class ClienteFinalCreate(ClienteFinalBase):
    """Schema para criação de cliente final"""
    pass

class ClienteFinalUpdate(BaseModel):
    """Schema para atualização de cliente final - todos campos opcionais"""
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    cpf_cnpj: Optional[str] = Field(None)  # Sem validação
    email: Optional[str] = Field(None, max_length=100)
    telefone: Optional[str] = Field(None, max_length=20)
    endereco: Optional[str] = Field(None, max_length=200)
    cidade: Optional[str] = Field(None, max_length=100)
    data_ultima_compra: Optional[date] = Field(None)
    valor_compra: Optional[Decimal] = Field(None, ge=0)

class ClienteFinalResponse(ClienteFinalBase):
    """Schema para resposta do cliente final"""
    cliente_finalid: int = Field(..., description="ID do cliente")
    
    class Config:
        from_attributes = True