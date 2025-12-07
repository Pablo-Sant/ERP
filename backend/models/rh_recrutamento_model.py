from sqlalchemy import Column, Integer, Date, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class Recrutamento(DBBaseModel):
    __tablename__ = "recrutamento"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, Sequence("rh.recrutamento_id_seq"), primary_key=True)

    # CORRIJA: Adicione ForeignKey
    colaborador_id = Column(Integer, ForeignKey("rh.colaboradores.id"), nullable=False)
    data_recrutamento = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)
    observacoes = Column(String(200))
    
    # Adicione o relacionamento
    colaborador = relationship("Colaborador", back_populates="recrutamentos")