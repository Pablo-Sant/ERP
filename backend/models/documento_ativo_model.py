from sqlalchemy import (
    Column, Integer, String, Text, Date, Numeric, Boolean,
    ForeignKey, DateTime, JSON, CheckConstraint, text, func, orm
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from core.configs import DBBaseModel
from typing import List
from models.ativos_model import Ativo

class DocumentoAtivo(DBBaseModel):
    __tablename__ = "documentos_ativos"
    __table_args__ = (
        CheckConstraint(
            "tipo_documento IN ('manual','certificado','garantia','desenho','foto','relatorio','outro')"
        ),
        {"schema": "am"}
    )

    id = Column(Integer, primary_key=True)
    id_ativo = Column(Integer, ForeignKey("am.ativos.id"), nullable=False)
    ativo = orm.relationship("Ativo", lazy='joined')
    tipo_documento = Column(String(50))
    nome_documento = Column(String(255), nullable=False)
    nome_arquivo = Column(String(255))
    caminho_arquivo = Column(String(500))
    tamanho_arquivo = Column(Integer)
    tipo_mime = Column(String(100))
    enviado_por = Column(Integer)
    data_envio = Column(DateTime(timezone=True), server_default=func.now())