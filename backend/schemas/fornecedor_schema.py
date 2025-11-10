from pydantic import BaseModel, EmailStr
from typing import Optional

class FornecedorBase(BaseModel):
    id_organizacao: int
    codigo: str
    nome: str
    tipo_fornecedor: Optional[str]
    pessoa_contato: Optional[str]
    telefone: Optional[str]
    email: Optional[EmailStr]
    endereco: Optional[str]
    cnpj: Optional[str]
    condicoes_pagamento: Optional[str]
    ativo: Optional[bool] = True

class FornecedorCreate(FornecedorBase):
    pass

class FornecedorResponse(FornecedorBase):
    id: int

    class Config:
        orm_mode = True
