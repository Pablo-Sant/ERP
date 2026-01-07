from decimal import Decimal
from typing import Optional, List, Annotated
from pydantic import BaseModel, StringConstraints, Field
from datetime import datetime, date

class FinanceiroFluxoCaixaBase(BaseModel):
    data: date
    saldo_inicial: Decimal
    entradas: Decimal
    saidas: Decimal
    saldo_final: Decimal


class FinanceiroFluxoCaixaCreate(FinanceiroFluxoCaixaBase):
    pass


class FinanceiroFluxoCaixaResponse(FinanceiroFluxoCaixaBase):
    id_fluxo: int

    class Config:
        from_attributes = True


class FinanceiroFluxoCaixaUpdate(BaseModel):
    """Schema para atualização parcial de fluxo de caixa"""
    data: Optional[date] = None
    saldo_inicial: Optional[Decimal] = None
    entradas: Optional[Decimal] = None
    saidas: Optional[Decimal] = None
    saldo_final: Optional[Decimal] = None
    
    class Config:
        from_attributes = True