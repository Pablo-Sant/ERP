from decimal import Decimal
from typing import Optional, List, Annotated
from pydantic import BaseModel, StringConstraints, Field
from datetime import datetime, date

class FiscalNotasFiscaisBase(BaseModel):
    numero_nota: Annotated[str, StringConstraints(max_length=50)]
    tipo: Annotated[str, StringConstraints(max_length=10)]
    valor_total: Decimal
    data_emissao: date
    chave_acesso: Optional[str] = None
    status: Optional[Annotated[str, StringConstraints(max_length=20)]] = "ativa"


class FiscalNotasFiscaisCreate(FiscalNotasFiscaisBase):
    pass


class FiscalNotasFiscaisResponse(FiscalNotasFiscaisBase):
    id_nota: int

    class Config:
        from_attributes = True