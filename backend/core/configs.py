import os
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
load_dotenv()


DBBaseModel = declarative_base()

class Settings(BaseSettings):
    API_V1_STR:str = '/api/v1'
    DB_URL:str 
    

    class Config:
        env_file = ".env" 
        case_sensitive = True


settings = Settings()


