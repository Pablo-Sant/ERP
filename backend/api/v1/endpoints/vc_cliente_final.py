from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.deps import get_current_user, get_session
from models.usuario_model import UsuarioModel
from services.cliente_final_service import ClienteFinalService
from schemas.vc_cliente_final_schema import ClienteFinalCreate, ClienteFinalUpdate, ClienteFinalResponse
from exceptions.usuarios_execeptions import ClienteNaoEncontrado

router = APIRouter()

@router.post('/', response_model=ClienteFinalResponse, status_code=201)
async def criar_cliente(payload: ClienteFinalCreate, db: AsyncSession = Depends(get_session)):
    
    try:
        return await ClienteFinalService.criar(payload, db)
    
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
    

@router.get('/', response_model=List[ClienteFinalResponse], status_code=200)
async def listar_clientes(usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    return await ClienteFinalService.get_all(usuario_logado, db)


@router.get('/{cliente_id}', response_model=ClienteFinalResponse, status_code=200)
async def buscar_por_id(cliente_id: int, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    cliente = await ClienteFinalService.get_by_id(usuario_logado, cliente_id, db)
    if not cliente:
        raise HTTPException(detail="Cliente não encontrado", status_code=404)
    return cliente


@router.get('/buscar/nome', response_model=List[ClienteFinalResponse], status_code=200)
async def buscar_por_nome(nome: str, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    return await ClienteFinalService.buscar_por_nome(usuario_logado, nome, db)


@router.put('/{cliente_id}', response_model=ClienteFinalResponse, status_code=200)
async def atualizar_cliente(cliente_id: int, payload: ClienteFinalUpdate, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    try:
        cliente = await ClienteFinalService.update(usuario_logado, cliente_id, payload, db)
        if not cliente:
            raise HTTPException(detail="Cliente não encontrado", status_code=404)
        return cliente
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
    

@router.delete('/{cliente_id}', status_code=204)
async def deletar_cliente(cliente_id: int, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    try:
        sucesso = await ClienteFinalService.delete(cliente_id, usuario_logado, db)
        if not sucesso:
            raise HTTPException(detail="Cliente não encontrado", status_code=404)
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
    

@router.patch('/{cliente_id}/compra', response_model=ClienteFinalResponse, status_code=200)
async def atualizar_compra(cliente_id: int, valor: float, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    try:
        return await ClienteFinalService.atualizar_dados_compra(cliente_id, valor, usuario_logado, db)
    except ClienteNaoEncontrado:
        raise HTTPException(detail="Cliente não encontrado", status_code=404)