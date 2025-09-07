from typing import List
from pydantic import BaseSettings, AnyHttpUrl
from sqlalchemy.ext.declarative import declarative_base



class Settings(BaseSettings):
    """Configurações gerais usadas na aplicação"""
    API_V1_STR:str = '/api/v1'
    DB_URL:str # O BaseSettings já importa automaticamente do .env, ent não precisa usar load_dotenv e os.getenv()
    DBBaseModel = declarative_base()

    class Config:
        env_file = ".env" # Carrega as variáveis de ambiente
        case_sensitive = True


settings = Settings()
