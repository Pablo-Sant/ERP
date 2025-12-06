# vc_api.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime

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

# ========== CLIENTE FINAL ==========
@router.post("/clientes/", response_model=ClienteFinalResponse, status_code=status.HTTP_201_CREATED)
def criar_cliente(cliente: ClienteFinalCreate, db: Session = Depends(get_db)):
    """Cria um novo cliente final"""
    db_cliente = ClienteFinal(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.get("/clientes/", response_model=List[ClienteFinalResponse])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os clientes finais"""
    clientes = db.query(ClienteFinal).offset(skip).limit(limit).all()
    return clientes

@router.get("/clientes/{cliente_id}", response_model=ClienteFinalResponse)
def obter_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtém um cliente final pelo ID"""
    cliente = db.query(ClienteFinal).filter(ClienteFinal.cliente_finalid == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.put("/clientes/{cliente_id}", response_model=ClienteFinalResponse)
def atualizar_cliente(
    cliente_id: int, 
    cliente_data: ClienteFinalBase, 
    db: Session = Depends(get_db)
):
    """Atualiza um cliente final"""
    cliente = db.query(ClienteFinal).filter(ClienteFinal.cliente_finalid == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    for key, value in cliente_data.dict(exclude_unset=True).items():
        setattr(cliente, key, value)
    
    db.commit()
    db.refresh(cliente)
    return cliente

@router.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Deleta um cliente final"""
    cliente = db.query(ClienteFinal).filter(ClienteFinal.cliente_finalid == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    db.delete(cliente)
    db.commit()
    return None

# ========== VENDEDOR ==========
@router.post("/vendedores/", response_model=VendedorResponse, status_code=status.HTTP_201_CREATED)
def criar_vendedor(vendedor: VendedorCreate, db: Session = Depends(get_db)):
    """Cria um novo vendedor"""
    db_vendedor = Vendedor(**vendedor.dict())
    db.add(db_vendedor)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

@router.get("/vendedores/", response_model=List[VendedorResponse])
def listar_vendedores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os vendedores"""
    vendedores = db.query(Vendedor).offset(skip).limit(limit).all()
    return vendedores

@router.get("/vendedores/{vendedor_id}", response_model=VendedorResponse)
def obter_vendedor(vendedor_id: int, db: Session = Depends(get_db)):
    """Obtém um vendedor pelo ID"""
    vendedor = db.query(Vendedor).filter(Vendedor.vendedorid == vendedor_id).first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    return vendedor

@router.put("/vendedores/{vendedor_id}", response_model=VendedorResponse)
def atualizar_vendedor(
    vendedor_id: int, 
    vendedor_data: VendedorBase, 
    db: Session = Depends(get_db)
):
    """Atualiza um vendedor"""
    vendedor = db.query(Vendedor).filter(Vendedor.vendedorid == vendedor_id).first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    
    for key, value in vendedor_data.dict(exclude_unset=True).items():
        setattr(vendedor, key, value)
    
    db.commit()
    db.refresh(vendedor)
    return vendedor

@router.delete("/vendedores/{vendedor_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_vendedor(vendedor_id: int, db: Session = Depends(get_db)):
    """Deleta um vendedor"""
    vendedor = db.query(Vendedor).filter(Vendedor.vendedorid == vendedor_id).first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    
    db.delete(vendedor)
    db.commit()
    return None

# ========== CONTRATO ==========
@router.post("/contratos/", response_model=ContratoResponse, status_code=status.HTTP_201_CREATED)
def criar_contrato(contrato: ContratoCreate, db: Session = Depends(get_db)):
    """Cria um novo contrato"""
    # Verifica se cliente existe
    cliente = db.query(ClienteFinal).filter(ClienteFinal.cliente_finalid == contrato.cliente_finalid).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Verifica se vendedor existe
    vendedor = db.query(Vendedor).filter(Vendedor.vendedorid == contrato.vendedorid).first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    
    db_contrato = Contrato(**contrato.dict())
    db.add(db_contrato)
    db.commit()
    db.refresh(db_contrato)
    return db_contrato

@router.get("/contratos/", response_model=List[ContratoResponse])
def listar_contratos(
    skip: int = 0, 
    limit: int = 100,
    cliente_id: Optional[int] = None,
    vendedor_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Lista todos os contratos com filtros opcionais"""
    query = db.query(Contrato)
    
    if cliente_id:
        query = query.filter(Contrato.cliente_finalid == cliente_id)
    if vendedor_id:
        query = query.filter(Contrato.vendedorid == vendedor_id)
    
    contratos = query.offset(skip).limit(limit).all()
    return contratos

@router.get("/contratos/{contrato_id}", response_model=ContratoResponse)
def obter_contrato(contrato_id: int, db: Session = Depends(get_db)):
    """Obtém um contrato pelo ID"""
    contrato = db.query(Contrato).filter(Contrato.contratoid == contrato_id).first()
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")
    return contrato

# ========== PEDIDO DE VENDA ==========
@router.post("/pedidos/", response_model=PedidoVendaResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(pedido: PedidoVendaCreate, db: Session = Depends(get_db)):
    """Cria um novo pedido de venda"""
    # Verifica se cliente existe
    cliente = db.query(ClienteFinal).filter(ClienteFinal.cliente_finalid == pedido.cliente_finalid).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Verifica se vendedor existe
    vendedor = db.query(Vendedor).filter(Vendedor.vendedorid == pedido.vendedorid).first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    
    db_pedido = PedidoVenda(**pedido.dict())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    
    # Cria automaticamente um histórico de compra
    historico = HistoricoCompra(
        cliente_finalid=pedido.cliente_finalid,
        pedido_id=db_pedido.pedidoid,
        data_compra=datetime.now().date()
    )
    db.add(historico)
    db.commit()
    
    # Atualiza dados do cliente
    cliente.data_ultima_compra = datetime.now().date()
    db.commit()
    
    return db_pedido

@router.get("/pedidos/", response_model=List[PedidoVendaResponse])
def listar_pedidos(
    skip: int = 0, 
    limit: int = 100,
    cliente_id: Optional[int] = None,
    vendedor_id: Optional[int] = None,
    status_pedido: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista todos os pedidos com filtros opcionais"""
    query = db.query(PedidoVenda)
    
    if cliente_id:
        query = query.filter(PedidoVenda.cliente_finalid == cliente_id)
    if vendedor_id:
        query = query.filter(PedidoVenda.vendedorid == vendedor_id)
    if status_pedido:
        query = query.filter(PedidoVenda.status == status_pedido)
    
    pedidos = query.offset(skip).limit(limit).all()
    return pedidos

@router.get("/pedidos/{pedido_id}", response_model=PedidoVendaResponse)
def obter_pedido(pedido_id: int, db: Session = Depends(get_db)):
    """Obtém um pedido pelo ID"""
    pedido = db.query(PedidoVenda).filter(PedidoVenda.pedidoid == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

@router.put("/pedidos/{pedido_id}/status", response_model=PedidoVendaResponse)
def atualizar_status_pedido(
    pedido_id: int, 
    status: str,
    db: Session = Depends(get_db)
):
    """Atualiza o status de um pedido"""
    pedido = db.query(PedidoVenda).filter(PedidoVenda.pedidoid == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    pedido.status = status
    db.commit()
    db.refresh(pedido)
    return pedido

# ========== HISTÓRICO DE COMPRA ==========
@router.post("/historicos/", response_model=HistoricoCompraResponse, status_code=status.HTTP_201_CREATED)
def criar_historico(historico: HistoricoCompraCreate, db: Session = Depends(get_db)):
    """Cria um novo histórico de compra"""
    # Verifica se cliente existe
    cliente = db.query(ClienteFinal).filter(ClienteFinal.cliente_finalid == historico.cliente_finalid).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Verifica se pedido existe (se fornecido)
    if historico.pedidoid:
        pedido = db.query(PedidoVenda).filter(PedidoVenda.pedidoid == historico.pedidoid).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    db_historico = HistoricoCompra(**historico.dict())
    db.add(db_historico)
    db.commit()
    db.refresh(db_historico)
    return db_historico

@router.get("/historicos/", response_model=List[HistoricoCompraResponse])
def listar_historicos(
    skip: int = 0, 
    limit: int = 100,
    cliente_id: Optional[int] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Lista históricos de compra com filtros"""
    query = db.query(HistoricoCompra)
    
    if cliente_id:
        query = query.filter(HistoricoCompra.cliente_final_id == cliente_id)
    if data_inicio:
        query = query.filter(HistoricoCompra.data_compra >= data_inicio)
    if data_fim:
        query = query.filter(HistoricoCompra.data_compra <= data_fim)
    
    historicos = query.order_by(HistoricoCompra.data_compra.desc()).offset(skip).limit(limit).all()
    return historicos

@router.get("/clientes/{cliente_id}/historicos", response_model=List[HistoricoCompraResponse])
def obter_historicos_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtém todos os históricos de compra de um cliente"""
    cliente = db.query(ClienteFinal).filter(ClienteFinal.cliente_finalid == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    return cliente.historicos_compra

# ========== PROSPECTO ==========
@router.post("/prospectos/", response_model=ProspectoResponse, status_code=status.HTTP_201_CREATED)
def criar_prospecto(prospecto: ProspectoCreate, db: Session = Depends(get_db)):
    """Cria um novo prospecto"""
    db_prospecto = Prospecto(**prospecto.dict())
    db.add(db_prospecto)
    db.commit()
    db.refresh(db_prospecto)
    return db_prospecto

@router.get("/prospectos/", response_model=List[ProspectoResponse])
def listar_prospectos(
    skip: int = 0, 
    limit: int = 100,
    fase_funil: Optional[str] = None,
    status_prospecto: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista todos os prospectos"""
    query = db.query(Prospecto)
    
    if fase_funil:
        query = query.filter(Prospecto.fase_funil == fase_funil)
    if status_prospecto:
        query = query.filter(Prospecto.status == status_prospecto)
    
    prospectos = query.offset(skip).limit(limit).all()
    return prospectos

@router.get("/prospectos/{prospecto_id}", response_model=ProspectoResponse)
def obter_prospecto(prospecto_id: int, db: Session = Depends(get_db)):
    """Obtém um prospecto pelo ID"""
    prospecto = db.query(Prospecto).filter(Prospecto.prospectoid == prospecto_id).first()
    if not prospecto:
        raise HTTPException(status_code=404, detail="Prospecto não encontrado")
    return prospecto

@router.put("/prospectos/{prospecto_id}/fase", response_model=ProspectoResponse)
def atualizar_fase_prospecto(
    prospecto_id: int, 
    fase_funil: str,
    db: Session = Depends(get_db)
):
    """Atualiza a fase do funil de um prospecto"""
    prospecto = db.query(Prospecto).filter(Prospecto.prospectoid == prospecto_id).first()
    if not prospecto:
        raise HTTPException(status_code=404, detail="Prospecto não encontrado")
    
    prospecto.fase_funil = fase_funil
    db.commit()
    db.refresh(prospecto)
    return prospecto

# ========== RELATÓRIOS E ESTATÍSTICAS ==========
@router.get("/relatorios/vendas-por-vendedor")
def relatorio_vendas_por_vendedor(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Relatório de vendas por vendedor"""
    query = db.query(
        Vendedor.nome,
        Vendedor.vendedorid,
        db.func.count(PedidoVenda.pedidoid).label("total_pedidos"),
        db.func.sum(HistoricoCompra.valor_compra).label("total_vendas")
    ).join(PedidoVenda, Vendedor.vendedorid == PedidoVenda.vendedorid)\
     .join(HistoricoCompra, PedidoVenda.pedidoid == HistoricoCompra.pedido_id)
    
    if data_inicio:
        query = query.filter(PedidoVenda.data_prevista_entrega >= data_inicio)
    if data_fim:
        query = query.filter(PedidoVenda.data_prevista_entrega <= data_fim)
    
    resultados = query.group_by(Vendedor.vendedorid, Vendedor.nome).all()
    
    return [
        {
            "vendedor_id": r.vendedorid,
            "vendedor_nome": r.nome,
            "total_pedidos": r.total_pedidos,
            "total_vendas": float(r.total_vendas) if r.total_vendas else 0
        }
        for r in resultados
    ]

@router.get("/relatorios/clientes-ativos")
def relatorio_clientes_ativos(db: Session = Depends(get_db)):
    """Relatório de clientes mais ativos"""
    clientes = db.query(
        ClienteFinal.nome,
        ClienteFinal.cliente_finalid,
        db.func.count(PedidoVenda.pedidoid).label("total_compras"),
        db.func.sum(HistoricoCompra.valor_compra).label("valor_total_compras"),
        db.func.max(PedidoVenda.data_prevista_entrega).label("ultima_compra")
    ).join(PedidoVenda, ClienteFinal.cliente_finalid == PedidoVenda.cliente_finalid)\
     .join(HistoricoCompra, PedidoVenda.pedidoid == HistoricoCompra.pedido_id)\
     .group_by(ClienteFinal.cliente_finalid, ClienteFinal.nome)\
     .order_by(db.func.sum(HistoricoCompra.valor_compra).desc())\
     .limit(10)\
     .all()
    
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

