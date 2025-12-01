from pydantic import BaseModel
from datetime import date
from typing import Optional

class ColaboradorBase(BaseModel):
    nome: str
    cpf: str
    email: Optional[str] = None
    funcao_id: Optional[int] = None
    data_contratacao: date
    carga_horaria: int
    data_de_nascimento: Optional[date] = None
    data_de_recrutamento: date
    salario: float


class ColaboradorCreate(ColaboradorBase):
    pass


class ColaboradorRead(ColaboradorBase):
    id: int

    class Config:
        orm_mode = True
