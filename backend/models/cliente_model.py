from core.configs import settings

from sqlalchemy import Column, String, Integer

# Tabelas para o banco de dados 

class ClienteModel(settings.DBBaseModel):
    __tablesname__ = "Clientes"

    id =  Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Nome = Column(String(100))



