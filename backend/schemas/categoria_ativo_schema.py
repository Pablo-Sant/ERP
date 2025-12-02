from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class CategoriaAtivoBase(BaseModel):
    id_organizacao: Optional[int] = Field(default=1)
    id_categoria_pai: Optional[int] = None
    codigo: str = Field(..., max_length=20)
    nome: str = Field(..., max_length=255)
    descricao: Optional[str] = None
    metodo_depreciacao: Optional[str] = Field(
        default="linha_reta",
        pattern="^(linha_reta|saldo_decrescente|unidades_producao|nenhum)$"
    )
    vida_util_padrao_anos: Optional[int] = Field(default=5, ge=1)
    taxa_residual_padrao: Optional[Decimal] = Field(default=0, ge=0, le=100)
    ativo: Optional[bool] = True

class CategoriaAtivoCreate(CategoriaAtivoBase):
    pass

class CategoriaAtivoUpdate(BaseModel):
    descricao: Optional[str] = None
    metodo_depreciacao: Optional[str] = Field(
        None,
        pattern="^(linha_reta|saldo_decrescente|unidades_producao|nenhum)$"
    )
    vida_util_padrao_anos: Optional[int] = Field(None, ge=1)
    taxa_residual_padrao: Optional[Decimal] = Field(None, ge=0, le=100)
    ativo: Optional[bool] = None

class CategoriaAtivoResponse(CategoriaAtivoBase):
    id: int
    nivel_hierarquia: int
    caminho_string: Optional[str]

    class Config:
        from_attributes = True