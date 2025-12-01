from pydantic import BaseModel
from datetime import date
from typing import Optional

class RecrutamentoBase(BaseModel):
    colaborador_id: int
    data_recrutamento: date
    status: str
    observacoes: Optional[str] = None


class RecrutamentoCreate(RecrutamentoBase):
    pass


class RecrutamentoRead(RecrutamentoBase):
    id: int

    class Config:
        orm_mode = True
