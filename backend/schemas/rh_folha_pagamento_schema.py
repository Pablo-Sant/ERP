from pydantic import BaseModel
from typing import Optional

class FolhaPagamentoBase(BaseModel):
    colaborador_id: int
    mes: int
    ano: int
    salario_base: float
    descontos: Optional[float] = None
    salario_liquido: float


class FolhaPagamentoCreate(FolhaPagamentoBase):
    pass


class FolhaPagamentoResponse(FolhaPagamentoBase):  # Mude de Read para Response
    id: int

    class Config:
        from_attributes = True  # Corrigido: de orm_mode para from_attributes


# ADICIONE ESTA CLASSE
class FolhaPagamentoUpdate(BaseModel):
    """Schema para atualização parcial de folha de pagamento"""
    colaborador_id: Optional[int] = None
    mes: Optional[int] = None
    ano: Optional[int] = None
    salario_base: Optional[float] = None
    descontos: Optional[float] = None
    salario_liquido: Optional[float] = None
    
    class Config:
        from_attributes = True