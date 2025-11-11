from datetime import date
from decimal import Decimal
from typing import Annotated, Optional, List
from pydantic import BaseModel, StringConstraints, Field

class PlanosManutencaoBase(BaseModel):
    id_organizacao: int
    nome: Annotated[str, StringConstraints(max_length=255)]
    descricao: Optional[str] = None
    tipo_manutencao: Optional[str] = Field(None, pattern=r"^(preventiva|corretiva|preditiva|condicional)?$")
    tipo_frequencia: Optional[str] = Field(None, pattern=r"^(diaria|semanal|mensal|trimestral|anual|base_medidor)?$")
    valor_frequencia: Optional[int] = None
    duracao_estimada_minutos: Optional[int] = None
    custo_estimado: Optional[Decimal] = None
    procedimentos: Optional[str] = None
    ativo: Optional[bool] = True


class PlanosManutencaoCreate(PlanosManutencaoBase):
    pass


class PlanosManutencaoResponse(PlanosManutencaoBase):
    id: int

    class Config:
        from_attributes = True