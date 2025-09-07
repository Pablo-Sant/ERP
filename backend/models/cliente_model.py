from core.configs import settings, DBBaseModel

from sqlalchemy import Column, String, Integer

# Tabelas para o banco de dados 

class ClienteModel(DBBaseModel):
    __tablename__ = "Clientes"

    id =  Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Nome = Column(String(100), nullable=False)
    Email = Column(String(120), unique=True, nullable=False, index=True)

    

