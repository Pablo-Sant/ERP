from sqlalchemy import Column, Integer, Date, String, Sequence
from core.configs import DBBaseModel

class Recrutamento(DBBaseModel):
    __tablename__ = "recrutamento"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, Sequence("rh.recrutamento_id_seq"), primary_key=True)

    colaborador_id = Column(Integer, nullable=False)
    data_recrutamento = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)
    observacoes = Column(String(200))
