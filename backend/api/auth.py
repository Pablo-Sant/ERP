# api/auth.py
"""from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from core.deps import get_session, get_current_user
from models.usuario import UsuarioModel
from schemas.auth_schema import LoginSchema, TokenSchema, UserResponseSchema
#from security import criar_token_jwt, verificar_senha
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenSchema)
async def login(
    login_data: LoginSchema,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        # BUSCAR APENAS OS CAMPOS NECESSÁRIOS PARA LOGIN
        query = select(
            UsuarioModel.id,
            UsuarioModel.email,
            UsuarioModel.nome,
            UsuarioModel.senha_hash,
            UsuarioModel.ativo,
            UsuarioModel.tipo_usuario
        ).filter(
            or_(
                UsuarioModel.email == login_data.username,
                UsuarioModel.nome == login_data.username
            )
        )
        
        result = await session.execute(query)
        usuario_data = result.first()  # Retorna uma tupla, não o objeto completo
        
        if not usuario_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário não encontrado"
            )

        # Desempacotar os dados
        user_id, email, nome, senha_hash, ativo, tipo_usuario = usuario_data

        # Verificar senha
        if not verificar_senha(login_data.password, senha_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha incorreta"
            )

        if not ativo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário inativo"
            )

        # Atualizar último login (usando query direta)
        from datetime import datetime
        update_query = select(UsuarioModel).where(UsuarioModel.id == user_id)
        update_result = await session.execute(update_query)
        usuario_obj = update_result.scalar_one()
        usuario_obj.ultimo_login = datetime.utcnow()
        await session.commit()

        # Criar token JWT
        token = criar_token_jwt(user_id)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user_id,
                "email": email,
                "nome": nome,
                "tipo_usuario": tipo_usuario
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
    return {"message": "Logout realizado com sucesso"}"""