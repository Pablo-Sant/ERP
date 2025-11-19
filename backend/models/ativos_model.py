from sqlalchemy import (
    Column, Integer, String, Text, Date, Numeric, Boolean,
    ForeignKey, DateTime, JSON, CheckConstraint, text, func, orm
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from core.configs import DBBaseModel
from typing import List
from models.categoria_ativo_model import CategoriaAtivo
from models.localizacao_model import Localizacao
from models.fornecedor_model import Fornecedor


class Ativo(DBBaseModel):
    __tablename__ = "ativos"
    __table_args__ = (
        CheckConstraint(
            "criticidade IN ('baixa','medio','alta','critico')"
        ),
        CheckConstraint(
            "status_ativo IN ('planejado','ativo','inativo','em_manutencao','baixado','descartado','perdido')"
        ),
        CheckConstraint("custo_aquisicao >= 0"),
        CheckConstraint("valor_atual >= 0"),
        CheckConstraint("valor_residual >= 0"),
        CheckConstraint("depreciacao_acumulada >= 0"),
        {"schema": "am"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    #uuid = Column(UUID(as_uuid=True), server_default=text("am.uuid_generate_v4()"))
    #id_organizacao = Column(Integer, nullable=False)
    id_categoria = Column(Integer, ForeignKey("am.categorias_ativos.id"), nullable=False)
    categoria = orm.relationship(CategoriaAtivo, lazy='joined')
    id_localizacao = Column(Integer, ForeignKey("am.localizacoes.id"), nullable=False)
    localizacao = orm.relationship("Localizacao", lazy='joined')
    numero_tag = Column(String(100), nullable=False)
    numero_serie = Column(String(100))
    modelo = Column(String(255))
    fabricante = Column(String(255))
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    status_ativo = Column(String(50), server_default=text("'ativo'"))
    criticidade = Column(String(20), server_default=text("'medio'"))
    data_aquisicao = Column(Date)
    custo_aquisicao = Column(Numeric(18, 2))
    numero_ordem_compra = Column(String(100))
    id_fornecedor = Column(Integer, ForeignKey("am.fornecedores.id"))
    fornecedores = orm.relationship(Fornecedor, lazy='joined')
    data_vencimento_garantia = Column(Date)
    vida_util_anos = Column(Integer)
    valor_residual = Column(Numeric(18, 2), server_default=text("0"))
    valor_atual = Column(Numeric(18, 2))
    depreciacao_acumulada = Column(Numeric(18, 2), server_default=text("0"))
    especificacoes = Column(JSONB)
    parametros_tecnicos = Column(JSONB)
    data_ativacao = Column(Date)
    data_desativacao = Column(Date)
    observacoes = Column(Text)
    criado_por = Column(Integer)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now())