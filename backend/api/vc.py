# vc_api.py - VERSÃO ASSÍNCRONA COMPLETA COM CORREÇÕES
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_, or_, text
from typing import List, Optional
from datetime import date, datetime
import traceback

from core.database import get_db
from models.vc_cliente_final_model import ClienteFinal
from models.vc_vendedor_model import Vendedor
from models.vc_contrato_model import Contrato
from models.vc_pedido_venda_model import PedidoVenda
from models.vc_historico_compra_model import HistoricoCompra
from models.vc_prospecto_model import Prospecto

from schemas.vc_cliente_final_schema import (
    ClienteFinalBase, ClienteFinalCreate, ClienteFinalResponse
)
from schemas.vc_vendedor_schema import (
    VendedorBase, VendedorCreate, VendedorResponse
)
from schemas.vc_contrato_schema import (
    ContratoBase, ContratoCreate, ContratoResponse
)
from schemas.vc_pedido_venda_schema import (
    PedidoVendaBase, PedidoVendaCreate, PedidoVendaResponse
)
from schemas.vc_historico_compra_schema import (
    HistoricoCompraBase, HistoricoCompraCreate, HistoricoCompraResponse
)
from schemas.vc_prospecto_schema import (
    ProspectoBase, ProspectoCreate, ProspectoResponse
)

router = APIRouter(prefix="/vc", tags=["Vendas e Contratos"])

# ========== ROTA DE TESTE ==========
@router.get("/test")
async def test_route():
    """Rota de teste para verificar se o módulo está funcionando"""
    return {
        "message": "Módulo VC está funcionando!", 
        "timestamp": datetime.now(),
        "status": "async"
    }

# ========== CLIENTE FINAL ==========
@router.post("/clientes/", response_model=ClienteFinalResponse, status_code=status.HTTP_201_CREATED)
async def criar_cliente(
    cliente: ClienteFinalCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Cria um novo cliente final"""
    db_cliente = ClienteFinal(**cliente.dict())
    db.add(db_cliente)
    await db.commit()
    await db.refresh(db_cliente)
    return db_cliente

@router.get("/clientes/", response_model=List[ClienteFinalResponse])
async def listar_clientes(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """Lista todos os clientes finais"""
    try:
        result = await db.execute(
            select(ClienteFinal)
            .offset(skip)
            .limit(limit)
            .order_by(ClienteFinal.nome)
            .distinct()
        )
        clientes = result.scalars().unique().all()
        return clientes
    except Exception as e:
        print(f"Erro em listar_clientes: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao listar clientes: {str(e)}"
        )

@router.get("/clientes/{cliente_id}", response_model=ClienteFinalResponse)
async def obter_cliente(
    cliente_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """Obtém um cliente final pelo ID"""
    result = await db.execute(
        select(ClienteFinal)
        .filter(ClienteFinal.cliente_finalid == cliente_id)
        .distinct()
    )
    cliente = result.scalars().unique().first()
    
    if not cliente:
        raise HTTPException(
            status_code=404, 
            detail="Cliente não encontrado"
        )
    return cliente

@router.put("/clientes/{cliente_id}", response_model=ClienteFinalResponse)
async def atualizar_cliente(
    cliente_id: int, 
    cliente_data: ClienteFinalBase, 
    db: AsyncSession = Depends(get_db)
):
    """Atualiza um cliente final"""
    result = await db.execute(
        select(ClienteFinal)
        .filter(ClienteFinal.cliente_finalid == cliente_id)
        .distinct()
    )
    cliente = result.scalars().unique().first()
    
    if not cliente:
        raise HTTPException(
            status_code=404, 
            detail="Cliente não encontrado"
        )
    
    for key, value in cliente_data.dict(exclude_unset=True).items():
        setattr(cliente, key, value)
    
    await db.commit()
    await db.refresh(cliente)
    return cliente

@router.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_cliente(
    cliente_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """Deleta um cliente final"""
    result = await db.execute(
        select(ClienteFinal)
        .filter(ClienteFinal.cliente_finalid == cliente_id)
        .distinct()
    )
    cliente = result.scalars().unique().first()
    
    if not cliente:
        raise HTTPException(
            status_code=404, 
            detail="Cliente não encontrado"
        )
    
    await db.delete(cliente)
    await db.commit()
    return None

# ========== VENDEDOR ==========
@router.post("/vendedores/", response_model=VendedorResponse, status_code=status.HTTP_201_CREATED)
async def criar_vendedor(
    vendedor: VendedorCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Cria um novo vendedor"""
    db_vendedor = Vendedor(**vendedor.dict())
    db.add(db_vendedor)
    await db.commit()
    await db.refresh(db_vendedor)
    return db_vendedor

@router.get("/vendedores/", response_model=List[VendedorResponse])
async def listar_vendedores(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """Lista todos os vendedores"""
    try:
        result = await db.execute(
            select(Vendedor)
            .offset(skip)
            .limit(limit)
            .order_by(Vendedor.nome)
            .distinct()
        )
        vendedores = result.scalars().unique().all()
        return vendedores
    except Exception as e:
        print(f"Erro em listar_vendedores: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao listar vendedores: {str(e)}"
        )

@router.get("/vendedores/{vendedor_id}", response_model=VendedorResponse)
async def obter_vendedor(
    vendedor_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """Obtém um vendedor pelo ID"""
    result = await db.execute(
        select(Vendedor)
        .filter(Vendedor.vendedorid == vendedor_id)
        .distinct()
    )
    vendedor = result.scalars().unique().first()
    
    if not vendedor:
        raise HTTPException(
            status_code=404, 
            detail="Vendedor não encontrado"
        )
    return vendedor

# ========== CONTRATO ==========
@router.post("/contratos/", response_model=ContratoResponse, status_code=status.HTTP_201_CREATED)
async def criar_contrato(
    contrato: ContratoCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Cria um novo contrato"""
    # Verifica se cliente existe
    cliente_result = await db.execute(
        select(ClienteFinal)
        .filter(ClienteFinal.cliente_finalid == contrato.cliente_finalid)
        .distinct()
    )
    cliente = cliente_result.scalars().unique().first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Verifica se vendedor existe
    vendedor_result = await db.execute(
        select(Vendedor)
        .filter(Vendedor.vendedorid == contrato.vendedorid)
        .distinct()
    )
    vendedor = vendedor_result.scalars().unique().first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    
    db_contrato = Contrato(**contrato.dict())
    db.add(db_contrato)
    await db.commit()
    await db.refresh(db_contrato)
    return db_contrato

@router.get("/contratos/", response_model=List[ContratoResponse])
async def listar_contratos(
    skip: int = 0, 
    limit: int = 100,
    cliente_id: Optional[int] = None,
    vendedor_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Lista todos os contratos com filtros opcionais"""
    try:
        query = select(Contrato)
        
        if cliente_id:
            query = query.filter(Contrato.cliente_finalid == cliente_id)
        if vendedor_id:
            query = query.filter(Contrato.vendedorid == vendedor_id)
        
        query = query.offset(skip).limit(limit).distinct()
        result = await db.execute(query)
        contratos = result.scalars().unique().all()
        return contratos
    except Exception as e:
        print(f"Erro em listar_contratos: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao listar contratos: {str(e)}"
        )

@router.get("/contratos/{contrato_id}", response_model=ContratoResponse)
async def obter_contrato(
    contrato_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """Obtém um contrato pelo ID"""
    result = await db.execute(
        select(Contrato)
        .filter(Contrato.contratoid == contrato_id)
        .distinct()
    )
    contrato = result.scalars().unique().first()
    
    if not contrato:
        raise HTTPException(
            status_code=404, 
            detail="Contrato não encontrado"
        )
    return contrato

# ========== PEDIDO DE VENDA ==========
@router.post("/pedidos/", response_model=PedidoVendaResponse, status_code=status.HTTP_201_CREATED)
async def criar_pedido(
    pedido: PedidoVendaCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Cria um novo pedido de venda"""
    # Verifica se cliente existe
    cliente_result = await db.execute(
        select(ClienteFinal)
        .filter(ClienteFinal.cliente_finalid == pedido.cliente_finalid)
        .distinct()
    )
    cliente = cliente_result.scalars().unique().first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Verifica se vendedor existe
    vendedor_result = await db.execute(
        select(Vendedor)
        .filter(Vendedor.vendedorid == pedido.vendedorid)
        .distinct()
    )
    vendedor = vendedor_result.scalars().unique().first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    
    db_pedido = PedidoVenda(**pedido.dict())
    db.add(db_pedido)
    await db.commit()
    await db.refresh(db_pedido)
    
    # Cria automaticamente um histórico de compra
    historico = HistoricoCompra(
        cliente_finalid=pedido.cliente_finalid,
        pedido_id=db_pedido.pedidoid,
        data_compra=datetime.now().date()
    )
    db.add(historico)
    await db.commit()
    
    # Atualiza dados do cliente
    cliente.data_ultima_compra = datetime.now().date()
    await db.commit()
    
    return db_pedido

@router.get("/pedidos/", response_model=List[PedidoVendaResponse])
async def listar_pedidos(
    skip: int = 0, 
    limit: int = 100,
    cliente_id: Optional[int] = None,
    vendedor_id: Optional[int] = None,
    status_pedido: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Lista todos os pedidos com filtros opcionais"""
    try:
        query = select(PedidoVenda)
        
        if cliente_id:
            query = query.filter(PedidoVenda.cliente_finalid == cliente_id)
        if vendedor_id:
            query = query.filter(PedidoVenda.vendedorid == vendedor_id)
        if status_pedido:
            query = query.filter(PedidoVenda.status == status_pedido)
        
        query = query.offset(skip).limit(limit).distinct()
        result = await db.execute(query)
        pedidos = result.scalars().unique().all()
        return pedidos
    except Exception as e:
        print(f"Erro em listar_pedidos: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao listar pedidos: {str(e)}"
        )

@router.get("/pedidos/{pedido_id}", response_model=PedidoVendaResponse)
async def obter_pedido(
    pedido_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """Obtém um pedido pelo ID"""
    result = await db.execute(
        select(PedidoVenda)
        .filter(PedidoVenda.pedidoid == pedido_id)
        .distinct()
    )
    pedido = result.scalars().unique().first()
    
    if not pedido:
        raise HTTPException(
            status_code=404, 
            detail="Pedido não encontrado"
        )
    return pedido

@router.put("/pedidos/{pedido_id}/status", response_model=PedidoVendaResponse)
async def atualizar_status_pedido(
    pedido_id: int, 
    status: str,
    db: AsyncSession = Depends(get_db)
):
    """Atualiza o status de um pedido"""
    result = await db.execute(
        select(PedidoVenda)
        .filter(PedidoVenda.pedidoid == pedido_id)
        .distinct()
    )
    pedido = result.scalars().unique().first()
    
    if not pedido:
        raise HTTPException(
            status_code=404, 
            detail="Pedido não encontrado"
        )
    
    pedido.status = status
    await db.commit()
    await db.refresh(pedido)
    return pedido

# ========== HISTÓRICO DE COMPRA ==========
@router.post("/historicos/", response_model=HistoricoCompraResponse, status_code=status.HTTP_201_CREATED)
async def criar_historico(
    historico: HistoricoCompraCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Cria um novo histórico de compra"""
    # Verifica se cliente existe
    cliente_result = await db.execute(
        select(ClienteFinal)
        .filter(ClienteFinal.cliente_finalid == historico.cliente_finalid)
        .distinct()
    )
    cliente = cliente_result.scalars().unique().first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Verifica se pedido existe (se fornecido)
    if historico.pedidoid:
        pedido_result = await db.execute(
            select(PedidoVenda)
            .filter(PedidoVenda.pedidoid == historico.pedidoid)
            .distinct()
        )
        pedido = pedido_result.scalars().unique().first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    db_historico = HistoricoCompra(**historico.dict())
    db.add(db_historico)
    await db.commit()
    await db.refresh(db_historico)
    return db_historico

@router.get("/historicos/", response_model=List[HistoricoCompraResponse])
async def listar_historicos(
    skip: int = 0, 
    limit: int = 100,
    cliente_id: Optional[int] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Lista históricos de compra com filtros"""
    try:
        query = select(HistoricoCompra)
        
        if cliente_id:
            query = query.filter(HistoricoCompra.cliente_finalid == cliente_id)
        if data_inicio:
            query = query.filter(HistoricoCompra.data_compra >= data_inicio)
        if data_fim:
            query = query.filter(HistoricoCompra.data_compra <= data_fim)
        
        query = query.order_by(HistoricoCompra.data_compra.desc())
        query = query.offset(skip).limit(limit).distinct()
        
        result = await db.execute(query)
        historicos = result.scalars().unique().all()
        return historicos
    except Exception as e:
        print(f"Erro em listar_historicos: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao listar históricos: {str(e)}"
        )

@router.get("/clientes/{cliente_id}/historicos", response_model=List[HistoricoCompraResponse])
async def obter_historicos_cliente(
    cliente_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """Obtém todos os históricos de compra de um cliente"""
    try:
        # Primeiro verifica se o cliente existe
        cliente_result = await db.execute(
            select(ClienteFinal)
            .filter(ClienteFinal.cliente_finalid == cliente_id)
            .distinct()
        )
        cliente = cliente_result.scalars().unique().first()
        
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        # Busca os históricos do cliente
        historicos_result = await db.execute(
            select(HistoricoCompra)
            .filter(HistoricoCompra.cliente_finalid == cliente_id)
            .order_by(HistoricoCompra.data_compra.desc())
            .distinct()
        )
        historicos = historicos_result.scalars().unique().all()
        
        return historicos
    except Exception as e:
        print(f"Erro em obter_historicos_cliente: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao obter históricos do cliente: {str(e)}"
        )

# ========== PROSPECTO ==========
@router.post("/prospectos/", response_model=ProspectoResponse, status_code=status.HTTP_201_CREATED)
async def criar_prospecto(
    prospecto: ProspectoCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Cria um novo prospecto"""
    db_prospecto = Prospecto(**prospecto.dict())
    db.add(db_prospecto)
    await db.commit()
    await db.refresh(db_prospecto)
    return db_prospecto

@router.get("/prospectos/", response_model=List[ProspectoResponse])
async def listar_prospectos(
    skip: int = 0, 
    limit: int = 100,
    fase_funil: Optional[str] = None,
    status_prospecto: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Lista todos os prospectos"""
    try:
        query = select(Prospecto)
        
        if fase_funil:
            query = query.filter(Prospecto.fase_funil == fase_funil)
        if status_prospecto:
            query = query.filter(Prospecto.status == status_prospecto)
        
        query = query.offset(skip).limit(limit).distinct()
        result = await db.execute(query)
        prospectos = result.scalars().unique().all()
        return prospectos
    except Exception as e:
        print(f"Erro em listar_prospectos: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao listar prospectos: {str(e)}"
        )

# ========== RELATÓRIOS E ESTATÍSTICAS ==========
@router.get("/relatorios/vendas-por-vendedor")
async def relatorio_vendas_por_vendedor(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Relatório de vendas por vendedor"""
    try:
        query = (
            select(
                Vendedor.nome,
                Vendedor.vendedorid,
                func.count(PedidoVenda.pedidoid).label("total_pedidos"),
                func.sum(HistoricoCompra.valor_compra).label("total_vendas")
            )
            .join(PedidoVenda, Vendedor.vendedorid == PedidoVenda.vendedorid)
            .join(HistoricoCompra, PedidoVenda.pedidoid == HistoricoCompra.pedidoid)
            .group_by(Vendedor.vendedorid, Vendedor.nome)
        )
        
        if data_inicio:
            query = query.filter(PedidoVenda.data_prevista_entrega >= data_inicio)
        if data_fim:
            query = query.filter(PedidoVenda.data_prevista_entrega <= data_fim)
        
        result = await db.execute(query)
        resultados = result.all()
        
        return [
            {
                "vendedor_id": r.vendedorid,
                "vendedor_nome": r.nome,
                "total_pedidos": r.total_pedidos,
                "total_vendas": float(r.total_vendas) if r.total_vendas else 0
            }
            for r in resultados
        ]
    except Exception as e:
        print(f"Erro em relatorio_vendas_por_vendedor: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao gerar relatório de vendas: {str(e)}"
        )

@router.get("/relatorios/clientes-ativos")
async def relatorio_clientes_ativos(db: AsyncSession = Depends(get_db)):
    """Relatório de clientes mais ativos"""
    try:
        query = (
            select(
                ClienteFinal.nome,
                ClienteFinal.cliente_finalid,
                func.count(PedidoVenda.pedidoid).label("total_compras"),
                func.sum(HistoricoCompra.valor_compra).label("valor_total_compras"),
                func.max(PedidoVenda.data_prevista_entrega).label("ultima_compra")
            )
            .join(PedidoVenda, ClienteFinal.cliente_finalid == PedidoVenda.cliente_finalid)
            .join(HistoricoCompra, PedidoVenda.pedidoid == HistoricoCompra.pedidoid)
            .group_by(ClienteFinal.cliente_finalid, ClienteFinal.nome)
            .order_by(func.sum(HistoricoCompra.valor_compra).desc())
            .limit(10)
        )
        
        result = await db.execute(query)
        clientes = result.all()
        
        return [
            {
                "cliente_id": c.cliente_finalid,
                "cliente_nome": c.nome,
                "total_compras": c.total_compras,
                "valor_total_compras": float(c.valor_total_compras) if c.valor_total_compras else 0,
                "ultima_compra": c.ultima_compra
            }
            for c in clientes
        ]
    except Exception as e:
        print(f"Erro em relatorio_clientes_ativos: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao gerar relatório de clientes ativos: {str(e)}"
        )

# ========== ENDPOINTS DE DIAGNÓSTICO ==========
@router.get("/debug/status")
async def debug_status():
    """Endpoint simples de status para debug"""
    return {
        "status": "vc_api funcionando",
        "timestamp": datetime.now().isoformat(),
        "module": "vc_api",
        "async": True
    }

@router.get("/debug/database")
async def debug_database(db: AsyncSession = Depends(get_db)):
    """Testa a conexão e estrutura do banco de dados"""
    try:
        # Teste 1: Conexão básica
        await db.execute(text("SELECT 1"))
        db_status = "connected"
        
        # Teste 2: Verifica se as tabelas existem
        tables_result = await db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'vc'
        """))
        tables = [row[0] for row in tables_result.fetchall()]
        
        # Teste 3: Conta registros em cada tabela
        counts = {}
        for table in tables:
            try:
                count_result = await db.execute(text(f"SELECT COUNT(*) FROM vc.{table}"))
                counts[table] = count_result.scalar()
            except Exception as e:
                counts[table] = f"error: {str(e)}"
        
        return {
            "status": "success",
            "database": "connected",
            "tables": tables,
            "record_counts": counts
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@router.get("/debug/clientes-test")
async def debug_clientes_test(db: AsyncSession = Depends(get_db)):
    """Teste direto da query de clientes"""
    try:
        # Método 1: Usando SQL puro
        sql_result = await db.execute(text("SELECT * FROM vc.cliente_final LIMIT 5"))
        sql_rows = sql_result.fetchall()
        
        # Método 2: Usando ORM
        orm_result = await db.execute(
            select(ClienteFinal).limit(5).distinct()
        )
        orm_rows = orm_result.scalars().unique().all()
        
        return {
            "sql_direct": [
                {"id": r[0], "nome": r[1], "email": r[3]} for r in sql_rows
            ],
            "orm_result": [
                {"id": r.cliente_finalid, "nome": r.nome, "email": r.email} for r in orm_rows
            ],
            "status": "success"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }