from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioCreate, UsuarioUpdate
from models.vc_cliente_final_model import ClienteFinal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from exceptions.usuarios_execeptions import NaoPossuiClientes, ClienteNaoEncontrado, UsuarioJaExistente, UsuarioNaoCadastrado
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso
from fastapi.security import OAuth2PasswordRequestForm



class UsuarioService:
    
    # empresário sobre clientes dele
    @staticmethod
    async def get_clientes(usuario_logado: UsuarioModel, db: AsyncSession):
        
        result = await db.execute(
            select(ClienteFinal).filter(ClienteFinal.usuario_id == usuario_logado.id)
        )
        
        clientes = result.scalars().all()
        
        if not clientes:
            raise NaoPossuiClientes
        
        return clientes
    
    @staticmethod
    async def get_cliente_by_id(id: int, usuario_logado: UsuarioModel, db: AsyncSession):
        
        result = await db.execute(
            select(ClienteFinal).filter(ClienteFinal.id == id, ClienteFinal.usuario_id == usuario_logado.id)
        )
        
        cliente = result.scalar_one_or_none()
        
        if not cliente:
            raise ClienteNaoEncontrado
        
        return cliente
    
    
    @staticmethod
    async def get_cliente_by_cpf(cpf_cnpj: str, usuario_logado: UsuarioModel, db: AsyncSession):
        
        result = await db.execute(
            select(ClienteFinal).filter(ClienteFinal.cpf_cnpj == cpf_cnpj, ClienteFinal.usuario_id == usuario_logado.id )
        )    
        
        cliente = result.scalar_one_or_none()
        
        if not cliente:
            raise ClienteNaoEncontrado
        
        return cliente
    
    
    @staticmethod
    async def del_cliente(id: int, usuario_logado: UsuarioModel, db: AsyncSession):
        
        cliente = await UsuarioService.get_cliente_by_id(id, usuario_logado, db)
        
        db.delete(cliente)
        await db.commit()
     
     
     # sobre o próprio empresário
     
    @staticmethod
    async def verificar_autorizacao(id: int, db: AsyncSession):
         
         result = await db.execute(
             select(UsuarioModel).filter(UsuarioModel.id == id)
         )
         
         usuario = result.scalar_one_or_none()
         
         return usuario
     
    # Garante que todas as alterações serão feitas no usuário logado, ou seja, usuário só poderá fazer alteções no próprio perfil
     
        
    @staticmethod   
    async def cadastrar(dto: UsuarioCreate, db: AsyncSession):
        
        usuario = await UsuarioService.verificar_existencia(dto.email, db)
        
        if usuario:
            raise UsuarioJaExistente
        
        data = dto.model_dump()
        senha_pura = data.pop('senha')
        
        usuario = UsuarioModel(**data, senha_hash = gerar_hash_senha(senha_pura))
        
        try:
            db.add(usuario)
            await db.commit()
            await db.refresh()
        
            return usuario
        
        except Exception as e:
            await db.rollback()
            raise e
        
    @staticmethod
    async def login(form_data: OAuth2PasswordRequestForm, db: AsyncSession) -> dict:
            
        usuario = await autenticar(form_data.username, form_data.password, db)
        
        # Usa excessões apenas no endpoint para ele decidir o HTTP
            
        return{
                
            'access_token': criar_token_acesso(sub=usuario.id),
            'token_type': 'bearer'
            
            }
        
        
    @staticmethod
    async def put_usuario(dto: UsuarioUpdate, usuario_logado: UsuarioModel, db: AsyncSession):
        
        usuario = await UsuarioService.verificar_existencia(usuario_logado.id, db)
        
        if not usuario:
            raise UsuarioNaoCadastrado
        
        
        data = dto.model_dump(exclude_unset=True)
        
        
        if 'senha' in data:
            data['senha'] = gerar_hash_senha(data['senha'])
            
        
        for campo, valor in data.items():
            setattr(usuario, campo, valor)
            
        try:
            await db.commit()
            await db.refresh(usuario)
        
            return usuario
        
        except Exception as e:
            await db.rollback()
            raise e
    
    
    
    @staticmethod
    async def del_usuario(usuario_logado: UsuarioModel, db: AsyncSession):
        
        usuario = await UsuarioService.verificar_autorizacao(usuario_logado.id, db) # Usuário irá fazer as alterações sobre ele msm
        
        if not usuario:
            raise UsuarioNaoCadastrado
        
        try:
            db.delete(usuario)
            await db.commit()
            
        except Exception as e:
            await db.rollback()
            raise e    
            
        