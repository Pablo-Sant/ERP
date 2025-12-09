# services/vendedor_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from models.vc_vendedor_model import Vendedor


class VendedorService:

    @staticmethod
    def _validar_cpf_cnpj(cpf_cnpj: Optional[str]) -> None:
        if cpf_cnpj is None or cpf_cnpj == "":
            raise ValueError('CPF/CNPJ é obrigatório para vendedor')
            
        numeros = ''.join(filter(str.isdigit, cpf_cnpj))
        
        if not numeros:
            raise ValueError('CPF/CNPJ deve conter apenas números')
        
        if len(numeros) not in (11, 14):
            raise ValueError(f'CPF deve ter 11 dígitos ou CNPJ 14 dígitos')
        
        if len(numeros) == 11:
            if numeros == numeros[0] * 11:
                raise ValueError('CPF inválido: todos os dígitos são iguais')
        elif len(numeros) == 14:
            if numeros == numeros[0] * 14:
                raise ValueError('CNPJ inválido: todos os dígitos são iguais')

    @staticmethod
    def _limpar_cpf_cnpj(cpf_cnpj: Optional[str]) -> Optional[str]:
        """Remove tudo que não for número do CPF/CNPJ"""
        if cpf_cnpj is None:
            return None
        return ''.join(filter(str.isdigit, cpf_cnpj))

    @staticmethod
    async def criar(dto, db: AsyncSession) -> Vendedor:
        VendedorService._validar_cpf_cnpj(dto.cpf_cnpj)
        
        dados = dto.model_dump()
        
        if 'cpf_cnpj' in dados and dados['cpf_cnpj'] is not None:
            cpf_cnpj_limpo = VendedorService._limpar_cpf_cnpj(dados['cpf_cnpj'])
            
            if not cpf_cnpj_limpo:
                raise ValueError('CPF/CNPJ deve conter apenas números')
                
            dados['cpf_cnpj'] = cpf_cnpj_limpo
            
            vendedor_existente = await VendedorService.buscar_por_cpf_cnpj(
                cpf_cnpj_limpo, db
            )
            if vendedor_existente:
                raise ValueError(f"CPF/CNPJ {cpf_cnpj_limpo} já cadastrado")
        
        novo_vendedor = Vendedor(**dados)
        
        db.add(novo_vendedor)
        await db.commit()
        await db.refresh(novo_vendedor)

        return novo_vendedor

    @staticmethod
    async def get_all(db: AsyncSession) -> List[Vendedor]:
        result = await db.execute(
            select(Vendedor).order_by(Vendedor.nome)
        )
        return result.unique().scalars().all()

    @staticmethod
    async def get_by_id(vendedor_id: int, db: AsyncSession) -> Optional[Vendedor]:
        result = await db.execute(
            select(Vendedor).filter(Vendedor.vendedorid == vendedor_id)
        )
        vendedor = result.scalars().first()
        
        if not vendedor:
            raise ValueError(f"Vendedor com ID {vendedor_id} não encontrado")
            
        return vendedor

    @staticmethod
    async def buscar_por_cpf_cnpj(cpf_cnpj: str, db: AsyncSession) -> Optional[Vendedor]:
        if not cpf_cnpj:
            return None
            
        cpf_cnpj_limpo = VendedorService._limpar_cpf_cnpj(cpf_cnpj)
        
        result = await db.execute(
            select(Vendedor).filter(Vendedor.cpf_cnpj == cpf_cnpj_limpo)
        )
        vendedor = result.scalars().first()
        
        if not vendedor:
            raise ValueError(f"Vendedor com CPF/CNPJ {cpf_cnpj} não encontrado")
            
        return vendedor

    @staticmethod
    async def buscar_por_nome(nome: str, db: AsyncSession) -> List[Vendedor]:
        if not nome or len(nome) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
            
        result = await db.execute(
            select(Vendedor)
            .filter(Vendedor.nome.ilike(f"%{nome}%"))
            .order_by(Vendedor.nome)
        )
        vendedores = result.unique().scalars().all()
        
        if not vendedores:
            raise ValueError(f"Nenhum vendedor encontrado com nome '{nome}'")
            
        return vendedores

    @staticmethod
    async def update(vendedor_id: int, dto, db: AsyncSession) -> Vendedor:
        vendedor = await VendedorService.get_by_id(vendedor_id, db)
        
        if dto.cpf_cnpj is not None:
            VendedorService._validar_cpf_cnpj(dto.cpf_cnpj)
            
            novo_cpf_cnpj_limpo = VendedorService._limpar_cpf_cnpj(dto.cpf_cnpj)
            cpf_cnpj_atual_limpo = VendedorService._limpar_cpf_cnpj(vendedor.cpf_cnpj)
            
            if novo_cpf_cnpj_limpo != cpf_cnpj_atual_limpo:
                vendedor_existente = await VendedorService.buscar_por_cpf_cnpj(
                    novo_cpf_cnpj_limpo, db
                )
                if vendedor_existente:
                    raise ValueError(f"CPF/CNPJ {dto.cpf_cnpj} já cadastrado")

  
        dados = dto.model_dump(exclude_unset=True)
        for campo, valor in dados.items():
            if campo == 'cpf_cnpj' and valor is not None:
                setattr(vendedor, campo, VendedorService._limpar_cpf_cnpj(valor))
            else:
                setattr(vendedor, campo, valor)

        await db.commit()
        await db.refresh(vendedor)
        return vendedor

    @staticmethod
    async def delete(vendedor_id: int, db: AsyncSession) -> bool:
        vendedor = await VendedorService.get_by_id(vendedor_id, db)
        
        if vendedor.contratos:
            raise ValueError("Não é possível excluir vendedor com contratos vinculados")
        
        if vendedor.pedidos:
            raise ValueError("Não é possível excluir vendedor com pedidos vinculados")

        await db.delete(vendedor)
        await db.commit()
        return True