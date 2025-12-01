from sqlalchemy import Column, Integer, Date, String, Sequence
from core.configs import DBBaseModel

class AvaliacaoDesempenho(DBBaseModel):
    __tablename__ = "avaliacao_desempenho"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, Sequence("rh.avaliacao_desempenho_id_seq"), primary_key=True)

    colaborador_id = Column(Integer, nullable=False)
    data_avaliacao = Column(Date, nullable=False)
    nota = Column(Integer, nullable=False)
    comentarios = Column(String(200))
