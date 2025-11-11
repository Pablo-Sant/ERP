from datetime import date
from decimal import Decimal
from typing import Annotated, Optional, List
from pydantic import BaseModel, StringConstraints, Field

class RegistrosCalibracaoBase(BaseModel):
    id_ativo: int
    data_calibracao: date
    data_proxima_calibracao: date
    calibrado_por: Optional[Annotated[str, StringConstraints(max_length=255)]] = None
    numero_certificado: Optional[Annotated[str, StringConstraints(max_length=100)]] = None
    padrao_utilizado: Optional[Annotated[str, StringConstraints(max_length=255)]] = None
    condicao_encontrada: Optional[str] = Field(None, pattern=r"^(dentro_especificacao|fora_especificacao|ajustado)?$")
    condicao_final: Optional[str] = Field(None, pattern=r"^(dentro_especificacao|fora_especificacao)?$")
    incerteza: Optional[Decimal] = None
    calibracao_aprovada: Optional[bool] = None
    observacoes: Optional[str] = None


class RegistrosCalibracaoCreate(RegistrosCalibracaoBase):
    pass


class RegistrosCalibracaoResponse(RegistrosCalibracaoBase):
    id: int

    class Config:
        from_attributes = True