from decimal import Decimal
from typing import Optional, List, Annotated
from pydantic import BaseModel, StringConstraints, Field
from datetime import datetime, date

class FiscalImpostosBase(BaseModel):
    id_nota: int
    tipo_imposto: Annotated[str, StringConstraints(max_length=20)]
    base_calculo: Decimal
    aliquota: Decimal
    valor: Decimal


class FiscalImpostosCreate(FiscalImpostosBase):
    pass


class FiscalImpostosResponse(FiscalImpostosBase):
    id_imposto: int

    class Config:
        from_attributes = True