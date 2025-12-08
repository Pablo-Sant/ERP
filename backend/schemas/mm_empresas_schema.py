# schemas/empresa_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EmpresaBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=255, description="Nome da empresa")
    cpf_cnpj: Optional[str] = Field(None, min_length=11, max_length=14, description="CPF/CNPJ")

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=255, description="Nome da empresa")
    cpf_cnpj: Optional[str] = Field(None, min_length=11, max_length=14, description="CPF/CNPJ")

class EmpresaResponse(EmpresaBase):
    """Schema para resposta da empresa"""
    id: int
    data_criacao: datetime
    
    class Config:
        from_attributes = True