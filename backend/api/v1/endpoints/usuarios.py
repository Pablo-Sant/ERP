from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.usuario_model import UsuarioModel
from core.deps import get_current_user, get_session
from schemas.usuario_schema import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from services.usuario_service import UsuarioService
from exceptions.usuarios_execeptions import NaoPossuiClientes, UsuarioJaExistente, UsuarioNaoCadastrado, SenhaIncorreta
from fastapi.security import OAuth2PasswordRequestForm
from schemas.token import TokenResponse



router = APIRouter()

@router.get('/me', response_model=UsuarioResponse, status_code=200)
async def get_usuarios(usuario_logado: UsuarioModel = Depends(get_current_user)):
    
    return usuario_logado



@router.post('/cadastro', response_model=UsuarioResponse, status_code=201)
async def cadastrar(payload: UsuarioCreate, db: AsyncSession = Depends(get_session)):
    
    try:
        return await UsuarioService.cadastrar(payload, db)
        
    except UsuarioJaExistente:
        raise HTTPException(detail='Usuário já cadastrado', status_code=status.HTTP_409_CONFLICT)
    
    
    
@router.post('/login', response_model=TokenResponse, status_code=200)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    
    try:
        return await UsuarioService.login(form_data, db)
    
    except (UsuarioNaoCadastrado, SenhaIncorreta):
        raise HTTPException(detail='Email ou senha incorretos', status_code=401)
        
    
    # Sempre enviar uma mensagem genérica para o cliente, ou seja, nunca especificar se é o email ou a senha que estão incorretos, pois isso diminui o escopo de atuação para uma possível burlagem 
    
@router.put('/', response_model=UsuarioResponse, status_code=201)
async def put(payload: UsuarioUpdate, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    
    try:
        return await UsuarioService.put_usuario(payload, usuario_logado, db)
    
    except UsuarioNaoCadastrado:
        raise HTTPException(detail='Usuário não cadastrado', status_code=400)
    
    
    
@router.delete('/', status_code=204)
async def delete(usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    
    try:
        return await UsuarioService.del_usuario(usuario_logado, db)
    
    except UsuarioNaoCadastrado:
        raise HTTPException(detail='Usuário não cadastrado', status_code=404)