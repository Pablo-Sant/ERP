from pydantic import BaseModel
from typing import Optional

class FuncaoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None


class FuncaoCreate(FuncaoBase):
    pass


class FuncaoRead(FuncaoBase):
    id: int

    class Config:
        orm_mode = True
