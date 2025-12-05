# sm_atendente_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class AtendenteBase(BaseModel):
    nome: str
    email: Optional[EmailStr] = None
    setor: Optional[str] = None

class AtendenteCreate(AtendenteBase):
    pass

class AtendenteResponse(AtendenteBase):
    id_atendente: int
    
    class Config:
        orm_mode = True
        from_attributes = True