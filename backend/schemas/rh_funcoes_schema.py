from pydantic import BaseModel, Field
from typing import Optional

class FuncaoBase(BaseModel):
    nome: str = Field(..., max_length=50)
    descricao: Optional[str] = Field(None, max_length=200)

class FuncaoCreate(FuncaoBase):
    pass

class FuncaoUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=50)
    descricao: Optional[str] = Field(None, max_length=200)

class FuncaoResponse(FuncaoBase):
    id: int
    
    class Config:
        from_attributes = True
