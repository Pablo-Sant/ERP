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
        from_attributes = True  # Alterado de orm_mode para from_attributes


# ADICIONE ESTA CLASSE
class CacheDadosBIUpdate(BaseModel):
    """Schema para atualização de cache de dados BI"""
    chave_cache: Optional[str] = None
    dados_json: Optional[Any] = None
    data_geracao: Optional[datetime] = None
    data_expiracao: Optional[datetime] = None
    
    class Config:
        from_attributes = True