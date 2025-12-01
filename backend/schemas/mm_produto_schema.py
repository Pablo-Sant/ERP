from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProdutoBase(BaseModel):
    empresa_id: int
    categoria_id: int
    nome: str
    descricao: Optional[str] = None

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    empresa_id: Optional[int] = None
    categoria_id: Optional[int] = None
    nome: Optional[str] = None
    descricao: Optional[str] = None

class ProdutoResponse(ProdutoBase):
    id: int
    empresa_id: int
    categoria_id: int
    nome: str
    descricao: str
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        orm_mode = True
