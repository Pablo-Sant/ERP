from pydantic import BaseModel
from typing import Optional

class BeneficioBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    valor: Optional[float] = None


class BeneficioCreate(BeneficioBase):
    pass


class BeneficioResponse(BeneficioBase):
    id: int

    class Config:
        from_attributes = True  # Corrigido: de orm_mode para from_attributes


# ADICIONE ESTA CLASSE
class BeneficioUpdate(BaseModel):
    """Schema para atualização parcial de benefício"""
    nome: Optional[str] = None
    descricao: Optional[str] = None
    valor: Optional[float] = None
    
    class Config:
        from_attributes = True