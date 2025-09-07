import os
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
load_dotenv()

url_database = os.getenv("DB_URL")

DBBaseModel = declarative_base()

class Settings(BaseSettings):
    """Configurações gerais usadas na aplicação"""
    API_V1_STR:str = '/api/v1'
    DB_URL:str = url_database  # O BaseSettings já importa automaticamente do .env, ent não precisa usar load_dotenv e os.getenv()
    

    class Config:
        env_file = ".env" # Carrega as variáveis de ambiente
        case_sensitive = True


settings = Settings()


