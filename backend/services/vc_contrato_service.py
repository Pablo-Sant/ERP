from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime, date
from models.vc_contrato_model import Contrato
from models.vc_cliente_final_model import ClienteFinal
from models.vc_vendedor_model import Vendedor


class ContratoService:
    

    @staticmethod
    async def _verificar_cliente_existe(cliente_finalid: int, db: AsyncSession) -> ClienteFinal:
        
        result = await db.execute(
            select(ClienteFinal).filter(ClienteFinal.cliente_finalid == cliente_finalid)
        )
        cliente = result.scalars().first()
        
        if not cliente:
            raise ValueError(f"Cliente final com ID {cliente_finalid} não encontrado")
            
        return cliente

    @staticmethod
    async def _verificar_vendedor_existe(vendedorid: int, db: AsyncSession) -> Vendedor:
       
        result = await db.execute(
            select(Vendedor).filter(Vendedor.vendedorid == vendedorid)
        )
        vendedor = result.scalars().first()
        
        if not vendedor:
            raise ValueError(f"Vendedor com ID {vendedorid} não encontrado")
            
        return vendedor

    @staticmethod
    async def _validar_datas(data_inicio: Optional[datetime], vencimento: Optional[date]) -> None:
        """Valida as datas do contrato"""
        if data_inicio and vencimento:
            if data_inicio.date() > vencimento:
                raise ValueError("Data de início não pode ser posterior à data de vencimento")
            
            if vencimento < date.today():
                raise ValueError("Data de vencimento não pode ser no passado")

    @staticmethod
    async def criar(dto, db: AsyncSession) -> Contrato:
        """Cria um novo contrato"""
        
        await ContratoService._verificar_cliente_existe(dto.cliente_finalid, db)
        
        
        await ContratoService._verificar_vendedor_existe(dto.vendedorid, db)
        
        
        await ContratoService._validar_datas(dto.data_inicio, dto.vencimento)
        
        dados = dto.model_dump()
        
        novo_contrato = Contrato(**dados)
        
        db.add(novo_contrato)
        await db.commit()
        await db.refresh(novo_contrato)

        return novo_contrato

    @staticmethod
    async def get_all(db: AsyncSession) -> List[Contrato]:
        """Retorna todos os contratos"""
        result = await db.execute(
            select(Contrato).order_by(Contrato.data_inicio.desc())
        )
        return result.unique().scalars().all()

    @staticmethod
    async def get_by_id(contrato_id: int, db: AsyncSession) -> Contrato:
        """Busca contrato por ID"""
        result = await db.execute(
            select(Contrato).filter(Contrato.contratoid == contrato_id)
        )
        contrato = result.scalars().first()
        
        if not contrato:
            raise ValueError(f"Contrato com ID {contrato_id} não encontrado")
            
        return contrato

    @staticmethod
    async def buscar_por_cliente(cliente_finalid: int, db: AsyncSession) -> List[Contrato]:
        """Busca contratos por cliente"""
        
        await ContratoService._verificar_cliente_existe(cliente_finalid, db)
        
        result = await db.execute(
            select(Contrato)
            .filter(Contrato.cliente_finalid == cliente_finalid)
            .order_by(Contrato.data_inicio.desc())
        )
        contratos = result.unique().scalars().all()
        
        if not contratos:
            raise ValueError(f"Nenhum contrato encontrado para o cliente ID {cliente_finalid}")
            
        return contratos

    @staticmethod
    async def buscar_por_vendedor(vendedorid: int, db: AsyncSession) -> List[Contrato]:

        await ContratoService._verificar_vendedor_existe(vendedorid, db)
        
        result = await db.execute(
            select(Contrato)
            .filter(Contrato.vendedorid == vendedorid)
            .order_by(Contrato.data_inicio.desc())
        )
        contratos = result.unique().scalars().all()
        
        if not contratos:
            raise ValueError(f"Nenhum contrato encontrado para o vendedor ID {vendedorid}")
            
        return contratos

    @staticmethod
    async def buscar_vencendo_em(data_vencimento: date, db: AsyncSession) -> List[Contrato]:
        """Busca contratos que vencem em uma determinada data"""
        result = await db.execute(
            select(Contrato)
            .filter(Contrato.vencimento == data_vencimento)
            .order_by(Contrato.data_inicio)
        )
        contratos = result.unique().scalars().all()
        
        if not contratos:
            raise ValueError(f"Nenhum contrato vencendo em {data_vencimento}")
            
        return contratos

    @staticmethod
    async def buscar_a_vencer(db: AsyncSession, dias: int = 30 ) -> List[Contrato]:
        
        from datetime import timedelta
        
        data_hoje = date.today()
        data_limite = data_hoje + timedelta(days=dias)
        
        result = await db.execute(
            select(Contrato)
            .filter(
                Contrato.vencimento >= data_hoje,
                Contrato.vencimento <= data_limite
            )
            .order_by(Contrato.vencimento)
        )
        contratos = result.unique().scalars().all()
        
        if not contratos:
            raise ValueError(f"Nenhum contrato vencendo nos próximos {dias} dias")
            
        return contratos

    @staticmethod
    async def update(contrato_id: int, dto, db: AsyncSession) -> Contrato:
        """Atualiza um contrato"""
        contrato = await ContratoService.get_by_id(contrato_id, db)
        
        
        if dto.cliente_finalid is not None and dto.cliente_finalid != contrato.cliente_finalid:
            await ContratoService._verificar_cliente_existe(dto.cliente_finalid, db)
        
        
        if dto.vendedorid is not None and dto.vendedorid != contrato.vendedorid:
            await ContratoService._verificar_vendedor_existe(dto.vendedorid, db)
        
        
        data_inicio = dto.data_inicio if dto.data_inicio is not None else contrato.data_inicio
        vencimento = dto.vencimento if dto.vencimento is not None else contrato.vencimento
        await ContratoService._validar_datas(data_inicio, vencimento)
        
        
        dados = dto.model_dump(exclude_unset=True)
        for campo, valor in dados.items():
            setattr(contrato, campo, valor)

        await db.commit()
        await db.refresh(contrato)
        return contrato

    @staticmethod
    async def delete(contrato_id: int, db: AsyncSession) -> bool:
        
        contrato = await ContratoService.get_by_id(contrato_id, db)
        
        
        if contrato.vencimento and (date.today() - contrato.vencimento).days > 30:
            raise ValueError("Não é possível excluir contratos vencidos há mais de 30 dias")

        await db.delete(contrato)
        await db.commit()
        return True

    @staticmethod
    async def renovar_contrato(contrato_id: int, nova_data_vencimento: date, db: AsyncSession) -> Contrato:
        
        contrato = await ContratoService.get_by_id(contrato_id, db)
        
        
        if nova_data_vencimento <= date.today():
            raise ValueError("Nova data de vencimento deve ser no futuro")
        
        if contrato.vencimento and nova_data_vencimento <= contrato.vencimento:
            raise ValueError("Nova data de vencimento deve ser posterior à data atual")
        
        contrato.vencimento = nova_data_vencimento
        await db.commit()
        await db.refresh(contrato)
        
        return contrato