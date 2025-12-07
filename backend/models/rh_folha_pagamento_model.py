from sqlalchemy import Column, Integer, Float, Sequence, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class FolhaPagamento(DBBaseModel):
    __tablename__ = "folha_pagamento"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, Sequence("rh.folha_pagamento_id_seq"), primary_key=True)

    # CORRIJA: Adicione ForeignKey
    colaborador_id = Column(Integer, ForeignKey("rh.colaboradores.id"), nullable=False)
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)

    salario_base = Column(Float, nullable=False)
    descontos = Column(Float)
    salario_liquido = Column(Float, nullable=False)
    
    # Adicione o relacionamento
    colaborador = relationship("Colaborador", back_populates="folhas_pagamento")