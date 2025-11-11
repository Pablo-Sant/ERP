from datetime import date
from decimal import Decimal
from typing import Annotated, Optional, List
from pydantic import BaseModel, StringConstraints, Field

class RegistrosDepreciacaoBase(BaseModel):
    id_ativo: int
    ano_fiscal: int
    periodo: int
    valor_depreciacao: Decimal
    depreciacao_acumulada: Decimal
    valor_liquido_contabil: Decimal
    data_calculo: date
    referencia_lancamento: Optional[Annotated[str, StringConstraints(max_length=100)]] = None


class RegistrosDepreciacaoCreate(RegistrosDepreciacaoBase):
    pass


class RegistrosDepreciacaoResponse(RegistrosDepreciacaoBase):
    id: int

    class Config:
        from_attributes = True