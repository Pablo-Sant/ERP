from sqlalchemy import (
    Column, Integer, String, Text, Numeric,
    CheckConstraint, text, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship
from core.configs import DBBaseModel

class CategoriaAtivo(DBBaseModel):
    __tablename__ = "categorias_ativos"
    __table_args__ = (
        CheckConstraint("taxa_residual_padrao >= 0 AND taxa_residual_padrao <= 100"),
        CheckConstraint(
            "metodo_depreciacao IN ('linha_reta','saldo_decrescente','unidades_producao','nenhum')"
        ),
        {"schema": "am"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_organizacao = Column(Integer, nullable=False, default=1)
    id_categoria_pai = Column(Integer, ForeignKey("am.categorias_ativos.id"))
    codigo = Column(String(20), nullable=False, unique=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    metodo_depreciacao = Column(String(50), server_default=text("'linha_reta'"))
    vida_util_padrao_anos = Column(Integer, server_default=text("5"))
    taxa_residual_padrao = Column(Numeric(5, 2), server_default=text("0"))
    nivel_hierarquia = Column(Integer, server_default=text("0"))
    caminho_string = Column(Text)
    ativo = Column(Boolean, server_default=text("true"))

    # Relacionamentos
    ativos = relationship("Ativo", back_populates="categoria")
    subcategorias = relationship(
        "CategoriaAtivo",
        back_populates="categoria_pai",
        remote_side=[id]
    )
    categoria_pai = relationship(
        "CategoriaAtivo",
        back_populates="subcategorias",
        remote_side=[id]
    )