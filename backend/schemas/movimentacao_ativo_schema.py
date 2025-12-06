from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MovimentacaoAtivoBase(BaseModel):
    id_ativo: int
    id_local_origem: Optional[int] = None
    id_local_destino: int
    tipo_movimentacao: Optional[str] = None
    motivo: Optional[str] = None
    movimentado_por: Optional[int] = None
    numero_referencia: Optional[str] = None


class MovimentacaoAtivoCreate(MovimentacaoAtivoBase):
    pass


class MovimentacaoAtivoResponse(MovimentacaoAtivoBase):
    id: int
    data_movimentacao: datetime

    class Config:
        from_attributes = True  # Corrigido: de orm_mode para from_attributes


# ADICIONE ESTA CLASSE
class MovimentacaoAtivoUpdate(BaseModel):
    """Schema para atualização parcial de movimentação de ativo"""
    id_ativo: Optional[int] = None
    id_local_origem: Optional[int] = None
    id_local_destino: Optional[int] = None
    tipo_movimentacao: Optional[str] = None
    motivo: Optional[str] = None
    movimentado_por: Optional[int] = None
    numero_referencia: Optional[str] = None
    data_movimentacao: Optional[datetime] = None
    
    class Config:
        from_attributes = True