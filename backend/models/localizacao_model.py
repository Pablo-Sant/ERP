from sqlalchemy import (
    Column, Integer, String, Text, Numeric, Boolean,
    ForeignKey, CheckConstraint, text
)
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class Localizacao(DBBaseModel):
    __tablename__ = "localizacoes"
    __table_args__ = (
        CheckConstraint(
            "tipo_local IN ('matriz','filial','armazem','fabrica','escritorio','campo','virtual')"
        ),
        {"schema": "am"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_organizacao = Column(Integer, nullable=False, default=1)
    id_local_pai = Column(Integer, ForeignKey("am.localizacoes.id"))
    codigo = Column(String(20), nullable=False, unique=True)
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

    # Relacionamentos
    ativos = relationship("Ativo", back_populates="localizacao")
    local_pai = relationship(
        "Localizacao",
        remote_side=[id],
        back_populates="sub_localizacoes"
    )
    sub_localizacoes = relationship(
        "Localizacao",
        back_populates="local_pai"
    )
    movimentacoes_origem = relationship(
        "MovimentacaoAtivo",
        foreign_keys="[MovimentacaoAtivo.id_local_origem]",
        back_populates="local_origem_rel"
    )
    movimentacoes_destino = relationship(
        "MovimentacaoAtivo",
        foreign_keys="[MovimentacaoAtivo.id_local_destino]",
        back_populates="local_destino_rel"
    )