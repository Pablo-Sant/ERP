from sqlalchemy import Column, Integer, String, Date, Float, Sequence
from core.configs import DBBaseModel

class Colaborador(DBBaseModel):
    __tablename__ = "colaboradores"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, Sequence("rh.colaboradores_id_seq"), primary_key=True)

    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), nullable=False)
    email = Column(String(100))

    funcao_id = Column(Integer)
    data_contratacao = Column(Date, nullable=False)
    carga_horaria = Column(Integer, nullable=False)

    data_de_nascimento = Column(Date)
    data_de_recrutamento = Column(Date, nullable=False)

    salario = Column(Float, nullable=False)
