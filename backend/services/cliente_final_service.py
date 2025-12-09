from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import date
from decimal import Decimal
from models.vc_cliente_final_model import ClienteFinal


class ClienteFinalService:
    

    @staticmethod
    def _validar_cpf_cnpj(cpf_cnpj: Optional[str]) -> None:
  
        if cpf_cnpj is None or cpf_cnpj == "":
            return    
        
        numeros = ''.join(filter(str.isdigit, cpf_cnpj))
        
        if not numeros:
            raise ValueError('CPF/CNPJ deve conter apenas números')
        
        if len(numeros) not in (11, 14):
            raise ValueError(f'CPF deve ter 11 dígitos ou CNPJ 14 dígitos. Recebido: {len(numeros)} dígitos')
        
        
        if len(numeros) == 11:
            
            if numeros == numeros[0] * 11:
                raise ValueError('CPF inválido: todos os dígitos são iguais')
   
        elif len(numeros) == 14:
         
            if numeros == numeros[0] * 14:
                raise ValueError('CNPJ inválido: todos os dígitos são iguais')
 

    @staticmethod
    def _limpar_cpf_cnpj(cpf_cnpj: Optional[str]) -> Optional[str]:
        if cpf_cnpj is None:
            return None
        
        return ''.join(filter(str.isdigit, cpf_cnpj))

    @staticmethod
    async def criar(dto, db: AsyncSession) -> ClienteFinal:

        ClienteFinalService._validar_cpf_cnpj(dto.cpf_cnpj)

        dados = dto.model_dump()
        
        if 'cpf_cnpj' in dados and dados['cpf_cnpj'] is not None:
            
            cpf_cnpj_limpo = ClienteFinalService._limpar_cpf_cnpj(dados['cpf_cnpj'])
            
            if not cpf_cnpj_limpo:
                raise ValueError('CPF/CNPJ deve conter apenas números')
                
            dados['cpf_cnpj'] = cpf_cnpj_limpo
            
            cliente_existente = await ClienteFinalService.buscar_por_cpf_cnpj(
                cpf_cnpj_limpo, db
            )
            if cliente_existente:
                raise ValueError(f"CPF/CNPJ {cpf_cnpj_limpo} já cadastrado")
        
        novo_cliente = ClienteFinal(**dados)
        
        db.add(novo_cliente)
        await db.commit()
        await db.refresh(novo_cliente)

        return novo_cliente

    @staticmethod
    async def get_all(db: AsyncSession) -> List[ClienteFinal]:

        result = await db.execute(
            select(ClienteFinal)
            .order_by(ClienteFinal.nome)
        )
        return result.unique().scalars().all()

    @staticmethod
    async def get_by_id(cliente_id: int, db: AsyncSession) -> Optional[ClienteFinal]:

        result = await db.execute(
            select(ClienteFinal)
            .filter(ClienteFinal.cliente_finalid == cliente_id)
        )
        return result.scalars().first()

    @staticmethod
    async def buscar_por_cpf_cnpj(cpf_cnpj: str, db: AsyncSession) -> Optional[ClienteFinal]:

        if not cpf_cnpj:
            return None
            
        result = await db.execute(
            select(ClienteFinal)
            .filter(ClienteFinal.cpf_cnpj == cpf_cnpj)
        )
        return result.scalars().first()

    @staticmethod
    async def buscar_por_nome(nome: str, db: AsyncSession) -> List[ClienteFinal]:

        result = await db.execute(
            select(ClienteFinal)
            .filter(ClienteFinal.nome.ilike(f"%{nome}%"))
            .order_by(ClienteFinal.nome)
        )
        return result.unique().scalars().all()

    @staticmethod
    async def update(cliente_id: int, dto, db: AsyncSession) -> Optional[ClienteFinal]:

        cliente = await ClienteFinalService.get_by_id(cliente_id, db)
        
        if not cliente:
            return None

        if dto.cpf_cnpj is not None:
            try:
                ClienteFinalService._validar_cpf_cnpj(dto.cpf_cnpj)
            except ValueError as e:
                raise ValueError(f"Erro de validação CPF/CNPJ: {str(e)}")
            
            novo_cpf_cnpj_limpo = ''.join(filter(str.isdigit, dto.cpf_cnpj))
            cpf_cnpj_atual_limpo = ''.join(filter(str.isdigit, cliente.cpf_cnpj or ""))
            
            if novo_cpf_cnpj_limpo != cpf_cnpj_atual_limpo:
                
                cliente_existente = await ClienteFinalService.buscar_por_cpf_cnpj(
                    novo_cpf_cnpj_limpo, db
                )
                if cliente_existente and cliente_existente.cliente_finalid != cliente_id:
                    raise ValueError(f"CPF/CNPJ {dto.cpf_cnpj} já cadastrado em outro cliente")

        dados = dto.model_dump(exclude_unset=True)
        for campo, valor in dados.items():
            if campo == 'cpf_cnpj' and valor is not None:
                setattr(cliente, campo, ''.join(filter(str.isdigit, valor)))
            else:
                setattr(cliente, campo, valor)

        await db.commit()
        await db.refresh(cliente)
        return cliente

    @staticmethod
    async def delete(cliente_id: int, db: AsyncSession) -> bool:

        cliente = await ClienteFinalService.get_by_id(cliente_id, db)
        
        if not cliente:
            return False

        if cliente.contratos:
            raise ValueError("Não é possível excluir cliente com contratos vinculados")
        
        if cliente.pedidos:
            raise ValueError("Não é possível excluir cliente com pedidos vinculados")

        await db.delete(cliente)
        await db.commit()
        return True

    @staticmethod
    async def verificar_cliente_existe(cliente_id: int, db: AsyncSession) -> bool:
        cliente = await ClienteFinalService.get_by_id(cliente_id, db)
        
        if not cliente:
            raise ValueError(f"Cliente com ID {cliente_id} não encontrado")
            
        return True

    @staticmethod
    async def atualizar_dados_compra(
        cliente_id: int, 
        valor_compra: float, 
        db: AsyncSession
    ) -> Optional[ClienteFinal]:

        cliente = await ClienteFinalService.get_by_id(cliente_id, db)
        
        if not cliente:
            return None

        cliente.data_ultima_compra = date.today()
        cliente.valor_compra = valor_compra

        await db.commit()
        await db.refresh(cliente)
        return cliente