from core.configs import settings

from sqlalchemy import Column, String, Integer

class ClienteModel(settings.DBBaseModel):
    __tablesname__ = "Clientes"

    id =  Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String(100))
    


