from pydantic import BaseModel
from typing import Optional

class CategoriaAtivoBase(BaseModel):
    id_organizacao: int
    codigo: str
    nome: str
    descricao: Optional[str]
    metodo_depreciacao: Optional[str] = "linha_reta"
    vida_util_padrao_anos: Optional[int] = 5
    taxa_residual_padrao: Optional[float] = 0.0
    nivel_hierarquia: Optional[str]
    caminho_string: Optional[str]

class CategoriaAtivoCreate(CategoriaAtivoBase):
    pass

class CategoriaAtivoResponse(CategoriaAtivoBase):
    id: int

    class Config:
        orm_mode = True
