from sqlalchemy import Column, Integer, Date, String, Sequence, ForeignKey, orm
from core.configs import DBBaseModel
from models.rh_colaboradores_model import Colaborador

class Recrutamento(DBBaseModel):
    __tablename__ = "recrutamento"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, Sequence("rh.recrutamento_id_seq"), primary_key=True)
    colaborador_id = Column(Integer, ForeignKey('rh.colaboradores.id'), nullable=False)
    colaborador = orm.relationship('Colaborador', lazy='joined')
    data_recrutamento = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)
    observacoes = Column(String(200))
    
    # Adicione o relacionamento
    colaborador = orm.relationship("Colaborador", back_populates="recrutamentos")