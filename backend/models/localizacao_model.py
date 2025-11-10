from sqlalchemy import (
    Column, Integer, String, Text, Date, Numeric, Boolean,
    ForeignKey, DateTime, JSON, CheckConstraint, text, func, orm
)
from core.configs import DBBaseModel
from typing import List

class Localizacao(DBBaseModel):
    __tablename__ = "localizacoes"
    __table_args__ = (
        CheckConstraint(
            "tipo_local IN ('matriz','filial','armazem','fabrica','escritorio','campo','virtual')"
        ),
        {"schema": "am"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_organizacao = Column(Integer, ForeignKey('organizao.id'), nullable=False)
    organizaco = orm.relationship('Organizacao', lazy='joined')
    id_local_pai = Column(Integer, ForeignKey('local_pai.id'))
    local_pai = orm.relationship('LocalPai', lazy='joined')
    codigo = Column(String(20), nullable=False)
    nome = Column(String(255), nullable=False)
    tipo_local = Column(String(50))
    endereco = Column(Text)
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    pessoa_contato = Column(String(255))
    telefone_contato = Column(String(20))
    ativo = Column(Boolean, server_default=text("true"))
    nivel_hierarquia = Column(Integer, server_default=text("0"))
    caminho_string = Column(Text)