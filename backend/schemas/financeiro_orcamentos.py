from decimal import Decimal
from typing import Optional, List, Annotated
from pydantic import BaseModel, StringConstraints, Field
from datetime import datetime, date

class FinanceiroOrcamentosBase(BaseModel):
    ano: int
    mes: int
    id_conta: int
    valor_previsto: Decimal
    valor_realizado: Decimal = Decimal("0.00")


class FinanceiroOrcamentosCreate(FinanceiroOrcamentosBase):
    pass


class FinanceiroOrcamentosResponse(FinanceiroOrcamentosBase):
    id_orcamento: int

    class Config:
        from_attributes = True


class FinanceiroOrcamentosUpdate(BaseModel):
    """Schema para atualização parcial de orçamentos"""
    ano: Optional[int] = None
    mes: Optional[int] = None
    id_conta: Optional[int] = None
    valor_previsto: Optional[Decimal] = None
    valor_realizado: Optional[Decimal] = None
    
    class Config:
        from_attributes = True