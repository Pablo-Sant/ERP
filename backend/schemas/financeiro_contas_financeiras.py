from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Annotated
from pydantic import BaseModel, StringConstraints, Field

class FinanceiroContasBase(BaseModel):
    nome: Annotated[str, StringConstraints(max_length=100)]
    tipo: Annotated[str, StringConstraints(max_length=50)]
    saldo_inicial: Decimal = Decimal("0.00")
    data_abertura: date
    ativo: bool = True


class FinanceiroContasCreate(FinanceiroContasBase):
    pass


class FinanceiroContasResponse(FinanceiroContasBase):
    id_conta: int

    class Config:
        from_attributes = True


class FinanceiroContasUpdate(BaseModel):
    nome: Optional[Annotated[str, StringConstraints(max_length=100)]] = None
    tipo: Optional[Annotated[str, StringConstraints(max_length=50)]] = None
    saldo_inicial: Optional[Decimal] = None
    data_abertura: Optional[date] = None
    ativo: Optional[bool] = None
    
    class Config:
        from_attributes = True