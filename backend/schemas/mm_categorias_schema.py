from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Union
from datetime import datetime

class CategoriaBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=255)
    descricao: Optional[str] = None
    categoria_pai_id: Optional[int] = None  # <- OBRIGATÓRIO: Union[int, None] ou Optional[int]
    status: str = Field(default="ativo")

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=255)
    descricao: Optional[str] = None
    categoria_pai_id: Optional[int] = None
    status: Optional[str] = None

class CategoriaResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    categoria_pai_id: Optional[int] = None  # <- Deve ser Optional[int]
    status: str
    data_criacao: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )