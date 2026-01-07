from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    email: EmailStr
    senha: str = Field(..., min_length=3, max_length=10)
    nome: str = Field(None, min_length=3, max_length=50)
    
    
class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr]
    senha: Optional[str] = Field(None, min_length=3, max_length=10)
    nome: Optional[str] = Field(None, min_length=3, max_length=50)
    
    
class UsuarioResponse(UsuarioBase):
    id: int
    email: EmailStr
    senha_hash: str
    nome: str
    data_criacao: datetime
    