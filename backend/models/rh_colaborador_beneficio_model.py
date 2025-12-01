from sqlalchemy import Column, Integer, Sequence
from core.configs import DBBaseModel

class ColaboradorBeneficio(DBBaseModel):
    __tablename__ = "colaborador_beneficios"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, Sequence("rh.colaborador_beneficios_id_seq"), primary_key=True)

    colaborador_id = Column(Integer, nullable=False)
    beneficio_id = Column(Integer, nullable=False)
