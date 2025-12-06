from decimal import Decimal
from typing import Optional, List, Annotated
from pydantic import BaseModel, StringConstraints, Field
from datetime import datetime, date

class FinanceiroLancamentosBase(BaseModel):
    id_conta: int
    tipo: Annotated[str, StringConstraints(max_length=10)]
    valor: Decimal
    descricao: Optional[str] = None
    data_lancamento: date
    origem_modulo: Optional[str] = None
    origem_id: Optional[int] = None
    created_at: Optional[datetime] = None


class FinanceiroLancamentosCreate(FinanceiroLancamentosBase):
    pass


class FinanceiroLancamentosResponse(FinanceiroLancamentosBase):
    id_lancamento: int

    class Config:
        from_attributes = True

class FinanceiroLancamentosUpdate(BaseModel):
    """Schema para atualização parcial de lançamentos financeiros"""
    id_conta: Optional[int] = None
    tipo: Optional[Annotated[str, StringConstraints(max_length=10)]] = None
    valor: Optional[Decimal] = None
    descricao: Optional[str] = None
    data_lancamento: Optional[date] = None
    origem_modulo: Optional[str] = None
    origem_id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True        