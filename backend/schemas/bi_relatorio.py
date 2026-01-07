from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class RelatorioBase(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    sql_query: Optional[str] = None
    tipo: Optional[str] = None
    status: Optional[str] = "ATIVO"
    data_criacao: Optional[datetime] = None


class RelatorioCreate(RelatorioBase):
    nome: str
    sql_query: str


class RelatorioRead(RelatorioBase):
    id_relatorio: int

    class Config:
        from_attributes = True  #



class RelatorioUpdate(BaseModel):
    """Schema para atualização parcial de relatório"""
    nome: Optional[str] = None
    descricao: Optional[str] = None
    sql_query: Optional[str] = None
    tipo: Optional[str] = None
    status: Optional[str] = None
    data_criacao: Optional[datetime] = None
    
    class Config:
        from_attributes = True