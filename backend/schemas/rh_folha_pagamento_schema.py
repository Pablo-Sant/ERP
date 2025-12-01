from pydantic import BaseModel
from typing import Optional

class FolhaPagamentoBase(BaseModel):
    colaborador_id: int
    mes: int
    ano: int
    salario_base: float
    descontos: Optional[float] = None
    salario_liquido: float


class FolhaPagamentoCreate(FolhaPagamentoBase):
    pass


class FolhaPagamentoRead(FolhaPagamentoBase):
    id: int

    class Config:
        orm_mode = True
