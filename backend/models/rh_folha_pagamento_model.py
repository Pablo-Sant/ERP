from sqlalchemy import Column, Integer, Float, Sequence, ForeignKey, orm
from core.configs import DBBaseModel
from models.rh_colaboradores_model import Colaborador

class FolhaPagamento(DBBaseModel):
    __tablename__ = "folha_pagamento"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, Sequence("rh.folha_pagamento_id_seq"), primary_key=True)

    colaborador_id = Column(Integer, ForeignKey('rh.colaboradores.id'), nullable=False)
    colaborador = orm.relationship('Colaborador', lazy='joined')
    
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)

    salario_base = Column(Float, nullable=False)
    descontos = Column(Float)
    salario_liquido = Column(Float, nullable=False)
    
    # Adicione o relacionamento
    colaborador = orm.relationship("Colaborador", back_populates="folhas_pagamento")