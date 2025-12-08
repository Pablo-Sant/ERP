# services/cliente_final_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from models.vc_cliente_final_model import ClienteFinal


class ClienteFinalService:
    

    @staticmethod
    async def criar(dto, db: AsyncSession) -> ClienteFinal:

        if dto.cpf_cnpj:
            cliente_existente = await ClienteFinalService.buscar_por_cpf_cnpj(
                dto.cpf_cnpj, db
            )
            if cliente_existente:
                raise ValueError(f"CPF/CNPJ {dto.cpf_cnpj} já cadastrado")

       
        novo_cliente = ClienteFinal(**dto.model_dump())
        
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
        return result.scalars().all()

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
        return result.scalars().all()

    @staticmethod
    async def update(cliente_id: int, dto, db: AsyncSession) -> Optional[ClienteFinal]:

        cliente = await ClienteFinalService.get_by_id(cliente_id, db)
        
        if not cliente:
            return None

        
        if dto.cpf_cnpj and dto.cpf_cnpj != cliente.cpf_cnpj:
            cliente_existente = await ClienteFinalService.buscar_por_cpf_cnpj(
                dto.cpf_cnpj, db
            )
            if cliente_existente and cliente_existente.cliente_finalid != cliente_id:
                raise ValueError(f"CPF/CNPJ {dto.cpf_cnpj} já cadastrado em outro cliente")

        
        for campo, valor in dto.model_dump(exclude_unset=True).items():
            setattr(cliente, campo, valor)

        await db.commit()
        await db.refresh(cliente)
        return cliente

    @staticmethod
    async def delete(cliente_id: int, db: AsyncSession) -> bool:
        cliente = await ClienteFinalService.get_by_id(cliente_id, db)
        
        if not cliente:
            return False

        
        if cliente.contratos or cliente.pedidos:
            raise ValueError("Não é possível excluir cliente com contratos ou pedidos vinculados")

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

        
        from datetime import date
        cliente.data_ultima_compra = date.today()
        
        cliente.valor_compra = valor_compra

        await db.commit()
        await db.refresh(cliente)
        return cliente