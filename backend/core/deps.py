from typing import Optional, AsyncGenerator

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select
from pydantic import BaseModel

from core.database import SessionLocal
from core.auth import oauth2_schema
from core.configs import settings
from models.usuario_model import UsuarioModel


class TokenData(BaseModel):
    user_id: Optional[str] = None
    
    
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
    
        try:
            yield session
        finally:
            await session.close()
        

async def get_current_user(db = Depends(get_session), token:str = Depends(oauth2_schema)) -> UsuarioModel:
    
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possível autenticar a credencial',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={'verify_aud': False}
        )
        
        user_id: str = payload.get('sub')
        if user_id is None:
            raise credential_exception
        token_data = TokenData(username=user_id)
    except JWTError:
        raise credential_exception
    
    result = await db.execute(
        select(UsuarioModel).filter(UsuarioModel.id == int(token_data.username)),
    )
    
    usuario = result.scalars().unique().one_or_none()
    
    if usuario is None:
        raise credential_exception
    
    return usuario
    
        