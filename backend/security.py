# security.py - USANDO pbkdf2_sha256 (mais confiável)
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

# Configurações
SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta-aqui-mude-em-producao")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Usar pbkdf2_sha256 que é mais confiável e não tem os problemas do bcrypt
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
    pbkdf2_sha256__default_rounds=30000
)

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    try:
        return pwd_context.verify(senha_plana, senha_hash)
    except Exception as e:
        print(f"Erro ao verificar senha: {e}")
        return False

def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)

def criar_token_jwt(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verificar_token_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None