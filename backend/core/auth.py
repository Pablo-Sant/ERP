from pytz import timezone
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from models.usuario_model import Usuario
from core.configs import settings
from core.security import verificar_senha
from pydantic import EmailStr

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
) 

async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> Optional[Usuario]:
    result = await db.execute( # O await só é usado quando for fazer uma operação no banco
        select(Usuario).filter(Usuario.email == email)
    )
    
    usuario = result.scalars().unique().one_or_none()
    
    if not usuario:
        return None
    
    if not verificar_senha(senha, usuario.senha):
        return None
    
    return usuario


def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3  Informações do payload
    payload = {}
    
    sp = timezone('America/Sao_Paulo')
    expira = datetime.now(tz=sp) + tempo_vida # calcula quando vai expirar, que é agora + 1 semana
    
    payload['type'] = tipo_token
    
    payload['exp'] = expira
    
    payload['iat'] = datetime.now(tz=sp)
    
    payload['sub'] = str(sub)
    
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def criar_token_acesso(sub: str) -> str:
    """
    https://jwt.io
    """
    return _criar_token(
        tipo_token='acess_token',
        tempo_vida=timedelta(minutes=settings.ACESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )