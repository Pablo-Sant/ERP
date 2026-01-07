from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClienteBase(BaseModel):
    nome: Optional[str] = None
    nome_fantasia: Optional[str] = None
    cnpj: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    ativo: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ClienteCreate(ClienteBase):
    nome: str
    cnpj: str


class ClienteRead(ClienteBase):
    id: int

    class Config:
        from_attributes = True  # Corrigido


# ADICIONE ESTA CLASSE
class ClienteUpdate(BaseModel):
    """Schema para atualização parcial de cliente"""
    nome: Optional[str] = None
    nome_fantasia: Optional[str] = None
    cnpj: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    ativo: Optional[bool] = None
    
    class Config:
        from_attributes = True