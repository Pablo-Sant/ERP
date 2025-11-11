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