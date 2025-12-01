from pydantic import BaseModel
from datetime import date
from typing import Optional

class AvaliacaoDesempenhoBase(BaseModel):
    colaborador_id: int
    data_avaliacao: date
    nota: int
    comentarios: Optional[str] = None


class AvaliacaoDesempenhoCreate(AvaliacaoDesempenhoBase):
    pass


class AvaliacaoDesempenhoRead(AvaliacaoDesempenhoBase):
    id: int

    class Config:
        orm_mode = True
