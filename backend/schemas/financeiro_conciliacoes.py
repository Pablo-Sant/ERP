from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Annotated
from pydantic import BaseModel, StringConstraints, Field

class FinanceiroConciliacoesBase(BaseModel):
    id_extrato: int
    id_lancamento: Optional[int] = None
    data_conciliacao: Optional[datetime] = None


class FinanceiroConciliacoesCreate(FinanceiroConciliacoesBase):
    pass


class FinanceiroConciliacoesResponse(FinanceiroConciliacoesBase):
    id_conciliacao: int

    class Config:
        from_attributes = True