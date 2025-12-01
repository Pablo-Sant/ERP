from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmpresaBase(BaseModel):
    id: int
    nome: str
    cpf_cnpj: str
    data_criacao: Optional[str] = None

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(BaseModel):
    id: Optional[int] = None
    nome: Optional[str] = None
    cpf_cnpj: Optional[str] = None

class EmpresaResponse(EmpresaBase):
    id: int
    nome: str
    cpf_cnpj: str
    data_criacao: datetime
    

    class Config:
        orm_mode = True
