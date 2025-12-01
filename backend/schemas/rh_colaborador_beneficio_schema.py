from pydantic import BaseModel

class ColaboradorBeneficioBase(BaseModel):
    colaborador_id: int
    beneficio_id: int


class ColaboradorBeneficioCreate(ColaboradorBeneficioBase):
    pass


class ColaboradorBeneficioRead(ColaboradorBeneficioBase):
    id: int

    class Config:
        orm_mode = True
