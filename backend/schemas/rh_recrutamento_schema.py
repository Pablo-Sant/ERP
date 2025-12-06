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


class RecrutamentoResponse(RecrutamentoBase):
    id: int

    class Config:
        from_attributes = True  # Corrigido: de orm_mode para from_attributes


# ADICIONE ESTA CLASSE
class RecrutamentoUpdate(BaseModel):
    """Schema para atualização parcial de recrutamento"""
    colaborador_id: Optional[int] = None
    data_recrutamento: Optional[date] = None
    status: Optional[str] = None
    observacoes: Optional[str] = None
    
    class Config:
        from_attributes = True