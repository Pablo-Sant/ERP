from sqlalchemy import (
    Column, Integer, String, Text, Date, Numeric, Boolean,
    ForeignKey, DateTime, JSON, CheckConstraint, text, func
)
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

    id = Column(Integer, primary_key=True)
    id_organizacao = Column(Integer, nullable=False)
    id_categoria_pai = Column(Integer)
    codigo = Column(String(20), nullable=False)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    metodo_depreciacao = Column(String(50), server_default=text("'linha_reta'"))
    vida_util_padrao_anos = Column(Integer, server_default=text("5"))
    taxa_residual_padrao = Column(Numeric(5, 2), server_default=text("0"))
    nivel_hierarquia = Column(Integer, server_default=text("0"))
    caminho_string = Column(Text)