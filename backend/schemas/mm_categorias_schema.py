from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoriaBase(BaseModel):
    nome: str
    descricao: str
    categoria_pai_id: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    categoria_pai_id: Optional[int] = None

class CategoriaResponse(CategoriaBase):
    id: int
    nome: str
    descricao: str
    categoria_pai_id: int

    class Config:
        orm_mode = True
