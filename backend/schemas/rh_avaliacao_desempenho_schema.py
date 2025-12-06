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


class AvaliacaoDesempenhoResponse(AvaliacaoDesempenhoBase):
    id: int

    class Config:
        from_attributes = True  # Corrigido: de orm_mode para from_attributes


# ADICIONE ESTA CLASSE
class AvaliacaoDesempenhoUpdate(BaseModel):
    """Schema para atualização parcial de avaliação de desempenho"""
    colaborador_id: Optional[int] = None
    data_avaliacao: Optional[date] = None
    nota: Optional[int] = None
    comentarios: Optional[str] = None
    
    class Config:
        from_attributes = True