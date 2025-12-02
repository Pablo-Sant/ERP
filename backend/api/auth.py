# api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from core.deps import get_session, get_current_user
from models.usuario import UsuarioModel
from schemas.auth_schema import LoginSchema, TokenSchema, UserResponseSchema
from security import criar_token_jwt, verificar_senha
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenSchema)
async def login(
    login_data: LoginSchema,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        # Buscar usuário pelo email (já que não temos username no modelo)
        query = select(UsuarioModel).filter(
            or_(
                UsuarioModel.email == login_data.username,
                UsuarioModel.nome == login_data.username  # Também permitir login pelo nome
            )
        )
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalar_one_or_none()

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário não encontrado"
            )

        # Verificar senha - note que a coluna é 'senha_hash'
        if not verificar_senha(login_data.password, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha incorreta"
            )

        if not usuario.ativo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário inativo"
            )

        # Atualizar último login
        from datetime import datetime
        usuario.ultimo_login = datetime.utcnow()
        await session.commit()

        # Criar token JWT
        token = criar_token_jwt(usuario.id)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": usuario.id,
                "email": usuario.email,
                "nome": usuario.nome,
                "tipo_usuario": usuario.tipo_usuario
            }
        }

@router.get("/me", response_model=UserResponseSchema)
async def get_current_user_info(
    current_user: UsuarioModel = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "nome": current_user.nome,
        "tipo_usuario": current_user.tipo_usuario
    }

@router.post("/logout")
async def logout():
    return {"message": "Logout realizado com sucesso"}