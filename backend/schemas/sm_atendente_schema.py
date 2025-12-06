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
        from_attributes = True  # Remova orm_mode, use apenas from_attributes


# ADICIONE ESTA CLASSE
class AtendenteUpdate(BaseModel):
    """Schema para atualização parcial de atendente"""
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    setor: Optional[str] = None
    
    class Config:
        from_attributes = True