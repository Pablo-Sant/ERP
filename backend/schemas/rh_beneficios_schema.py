from pydantic import BaseModel
from typing import Optional

class BeneficioBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    valor: Optional[float] = None


class BeneficioCreate(BeneficioBase):
    pass


class BeneficioRead(BeneficioBase):
    id: int

    class Config:
        orm_mode = True
