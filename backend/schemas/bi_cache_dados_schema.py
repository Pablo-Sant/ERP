from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class CacheDadosBIBase(BaseModel):
    chave_cache: Optional[str] = None
    dados_json: Optional[Any] = None
    data_geracao: Optional[datetime] = None
    data_expiracao: Optional[datetime] = None


class CacheDadosBICreate(CacheDadosBIBase):
    chave_cache: str
    dados_json: Any


class CacheDadosBIRead(CacheDadosBIBase):
    id_cache: int

    class Config:
        orm_mode = True