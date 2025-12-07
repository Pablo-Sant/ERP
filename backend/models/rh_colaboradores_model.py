from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class Colaborador(DBBaseModel):
    __tablename__ = "colaboradores"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, primary_key=True)
    
    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), nullable=False)
    email = Column(String(100))
    
    funcao_id = Column(Integer, ForeignKey("rh.funcoes.id"))
    data_contratacao = Column(Date, nullable=False)
    carga_horaria = Column(Integer, nullable=False)
    
    data_de_nascimento = Column(Date)
    data_de_recrutamento = Column(Date, nullable=False)
    
    salario = Column(Float, nullable=False)
    
    
    ativo = Column(Integer, default=1, server_default="1")  
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    
    funcao_rel = relationship("Funcao", back_populates="colaboradores")
    beneficios = relationship("ColaboradorBeneficio", back_populates="colaborador")
    folhas_pagamento = relationship("FolhaPagamento", back_populates="colaborador")
    recrutamentos = relationship("Recrutamento", back_populates="colaborador")
    avaliacoes = relationship("AvaliacaoDesempenho", back_populates="colaborador")