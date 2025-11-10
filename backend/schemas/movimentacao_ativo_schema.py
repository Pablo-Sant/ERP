from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MovimentacaoAtivoBase(BaseModel):
    id_ativo: int
    id_local_origem: Optional[int]
    id_local_destino: int
    tipo_movimentacao: Optional[str]
    motivo: Optional[str]
    movimentado_por: Optional[int]
    numero_referencia: Optional[str]

class MovimentacaoAtivoCreate(MovimentacaoAtivoBase):
    pass

class MovimentacaoAtivoResponse(MovimentacaoAtivoBase):
    id: int
    data_movimentacao: datetime

    class Config:
        orm_mode = True
