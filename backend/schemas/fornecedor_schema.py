from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class FornecedorBase(BaseModel):
    codigo: str = Field(..., max_length=20)
    nome: str = Field(..., max_length=255)
    tipo_fornecedor: Optional[str] = Field(
        None,
        pattern="^(fabricante|fornecedor|prestador_servico|distribuidor)$"
    )
    pessoa_contato: Optional[str] = Field(None, max_length=255)
    telefone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    endereco: Optional[str] = None
    cnpj: Optional[str] = Field(None, max_length=20)
    condicoes_pagamento: Optional[str] = Field(None, max_length=100)
    ativo: Optional[bool] = True

class FornecedorCreate(FornecedorBase):
    pass

class FornecedorUpdate(BaseModel):
    pessoa_contato: Optional[str] = Field(None, max_length=255)
    telefone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    endereco: Optional[str] = None
    ativo: Optional[bool] = None

class FornecedorResponse(FornecedorBase):
    id: int

    class Config:
        from_attributes = True