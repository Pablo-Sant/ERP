from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Annotated
from pydantic import BaseModel, StringConstraints, Field

class FinanceiroExtratosBancariosBase(BaseModel):
    id_conta: int
    data_movimento: date
    descricao: Optional[str] = None
    valor: Decimal
    tipo: Annotated[str, StringConstraints(max_length=10)]
    conciliado: bool = False


class FinanceiroExtratosBancariosCreate(FinanceiroExtratosBancariosBase):
    pass


class FinanceiroExtratosBancariosResponse(FinanceiroExtratosBancariosBase):
    id_extrato: int

    class Config:
        from_attributes = True


class FinanceiroExtratosBancariosUpdate(BaseModel):
    """Schema para atualização parcial de extratos bancários"""
    id_conta: Optional[int] = None
    data_movimento: Optional[date] = None
    descricao: Optional[str] = None
    valor: Optional[Decimal] = None
    tipo: Optional[Annotated[str, StringConstraints(max_length=10)]] = None
    conciliado: Optional[bool] = None
    
    class Config:
        from_attributes = True