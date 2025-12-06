# sm_api.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import case
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, extract
from typing import List, Optional
from datetime import datetime, date, timedelta

from core.database import get_db
from models.sm_atendente_model import Atendente
from models.sm_ticket_atendimento_model import TicketAtendimento
from models.sm_solicitacao_troca_model import SolicitacaoTroca
from models.sm_views_models import (
    VwDashboardServicos,
    VwTicketsAbertos,
    VwTrocasPendentes,
    VwHistoricoCliente,
    VwMetricasMensais,
    VwAnaliseTiposAtendimento,
    VwTempoResolucao,
    VwPerformanceAtendentes
)

from schemas.sm_atendente_schema import (
    AtendenteBase, AtendenteCreate, AtendenteResponse
)
from schemas.sm_ticket_atendimento_schema import (
    TicketAtendimentoBase, TicketAtendimentoCreate, 
    TicketAtendimentoResponse, TicketAtendimentoUpdate
)
from schemas.sm_solicitacao_troca_schema import (
    SolicitacaoTrocaBase, SolicitacaoTrocaCreate,
    SolicitacaoTrocaResponse, SolicitacaoTrocaUpdate
)
from schemas.sm_views_schema import (
    DashboardServicosResponse,
    TicketAbertoResponse,
    TrocaPendenteResponse,
    HistoricoClienteResponse,
    MetricasMensaisResponse,
    AnaliseTiposAtendimentoResponse,
    TempoResolucaoResponse,
    PerformanceAtendentesResponse
)

router = APIRouter(prefix="/sm", tags=["Service Management"])

# ========== ATENDENTES ==========
@router.post("/atendentes/", response_model=AtendenteResponse, status_code=status.HTTP_201_CREATED)
def criar_atendente(atendente: AtendenteCreate, db: Session = Depends(get_db)):
    """Cria um novo atendente"""
    db_atendente = Atendente(**atendente.dict())
    db.add(db_atendente)
    db.commit()
    db.refresh(db_atendente)
    return db_atendente

@router.get("/atendentes/", response_model=List[AtendenteResponse])
def listar_atendentes(
    skip: int = 0, 
    limit: int = 100,
    setor: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista todos os atendentes com filtro opcional por setor"""
    query = db.query(Atendente)
    
    if setor:
        query = query.filter(Atendente.setor == setor)
    
    atendentes = query.offset(skip).limit(limit).all()
    return atendentes

@router.get("/atendentes/{atendente_id}", response_model=AtendenteResponse)
def obter_atendente(atendente_id: int, db: Session = Depends(get_db)):
    """Obtém um atendente pelo ID"""
    atendente = db.query(Atendente).filter(Atendente.id_atendente == atendente_id).first()
    if not atendente:
        raise HTTPException(status_code=404, detail="Atendente não encontrado")
    return atendente

@router.put("/atendentes/{atendente_id}", response_model=AtendenteResponse)
def atualizar_atendente(
    atendente_id: int,
    atendente_data: AtendenteBase,
    db: Session = Depends(get_db)
):
    """Atualiza um atendente"""
    atendente = db.query(Atendente).filter(Atendente.id_atendente == atendente_id).first()
    if not atendente:
        raise HTTPException(status_code=404, detail="Atendente não encontrado")
    
    for key, value in atendente_data.dict(exclude_unset=True).items():
        setattr(atendente, key, value)
    
    db.commit()
    db.refresh(atendente)
    return atendente

@router.delete("/atendentes/{atendente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_atendente(atendente_id: int, db: Session = Depends(get_db)):
    """Deleta um atendente"""
    atendente = db.query(Atendente).filter(Atendente.id_atendente == atendente_id).first()
    if not atendente:
        raise HTTPException(status_code=404, detail="Atendente não encontrado")
    
    db.delete(atendente)
    db.commit()
    return None

# ========== TICKETS DE ATENDIMENTO ==========
@router.post("/tickets/", response_model=TicketAtendimentoResponse, status_code=status.HTTP_201_CREATED)
def criar_ticket(ticket: TicketAtendimentoCreate, db: Session = Depends(get_db)):
    """Cria um novo ticket de atendimento"""
    # Verificar se o cliente existe (usando o módulo VC)
    from models.vc_cliente_final_model import ClienteFinal
    cliente = db.query(ClienteFinal).filter(ClienteFinal.cliente_finalid == ticket.id_cliente_final).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Verificar se o pedido existe (se fornecido)
    if ticket.id_pedido:
        from models.vc_pedido_venda_model import PedidoVenda
        pedido = db.query(PedidoVenda).filter(PedidoVenda.pedidoid == ticket.id_pedido).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    db_ticket = TicketAtendimento(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.get("/tickets/", response_model=List[TicketAtendimentoResponse])
def listar_tickets(
    skip: int = 0,
    limit: int = 100,
    cliente_id: Optional[int] = None,
    status_ticket: Optional[str] = None,
    tipo: Optional[str] = None,
    prioridade: Optional[str] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Lista tickets de atendimento com diversos filtros"""
    query = db.query(TicketAtendimento)
    
    if cliente_id:
        query = query.filter(TicketAtendimento.id_cliente_final == cliente_id)
    if status_ticket:
        query = query.filter(TicketAtendimento.status == status_ticket)
    if tipo:
        query = query.filter(TicketAtendimento.tipo == tipo)
    if prioridade:
        query = query.filter(TicketAtendimento.prioridade == prioridade)
    if data_inicio:
        query = query.filter(TicketAtendimento.data_abertura >= data_inicio)
    if data_fim:
        # Adiciona 1 dia para incluir o dia final completo
        data_fim_completa = datetime.combine(data_fim, datetime.max.time())
        query = query.filter(TicketAtendimento.data_abertura <= data_fim_completa)
    
    tickets = query.order_by(TicketAtendimento.data_abertura.desc()).offset(skip).limit(limit).all()
    return tickets

@router.get("/tickets/{ticket_id}", response_model=TicketAtendimentoResponse)
def obter_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Obtém um ticket pelo ID"""
    ticket = db.query(TicketAtendimento).filter(TicketAtendimento.id_ticket == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    return ticket

@router.put("/tickets/{ticket_id}", response_model=TicketAtendimentoResponse)
def atualizar_ticket(
    ticket_id: int,
    ticket_data: TicketAtendimentoUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um ticket de atendimento"""
    ticket = db.query(TicketAtendimento).filter(TicketAtendimento.id_ticket == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    # Se status for alterado para RESOLVIDO e data_resolucao não estiver definida, definir agora
    if ticket_data.status == "RESOLVIDO" and not ticket_data.data_resolucao and not ticket.data_resolucao:
        ticket_data.data_resolucao = datetime.now()
    
    for key, value in ticket_data.dict(exclude_unset=True).items():
        setattr(ticket, key, value)
    
    db.commit()
    db.refresh(ticket)
    return ticket

@router.delete("/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Deleta um ticket de atendimento"""
    ticket = db.query(TicketAtendimento).filter(TicketAtendimento.id_ticket == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    db.delete(ticket)
    db.commit()
    return None

@router.patch("/tickets/{ticket_id}/status", response_model=TicketAtendimentoResponse)
def atualizar_status_ticket(
    ticket_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Atualiza apenas o status de um ticket"""
    ticket = db.query(TicketAtendimento).filter(TicketAtendimento.id_ticket == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    ticket.status = status
    
    # Se status for RESOLVIDO, definir data de resolução
    if status == "RESOLVIDO" and not ticket.data_resolucao:
        ticket.data_resolucao = datetime.now()
    
    db.commit()
    db.refresh(ticket)
    return ticket

# ========== SOLICITAÇÕES DE TROCA ==========
@router.post("/trocas/", response_model=SolicitacaoTrocaResponse, status_code=status.HTTP_201_CREATED)
def criar_solicitacao_troca(troca: SolicitacaoTrocaCreate, db: Session = Depends(get_db)):
    """Cria uma nova solicitação de troca"""
    # Verificar se o ticket existe
    ticket = db.query(TicketAtendimento).filter(TicketAtendimento.id_ticket == troca.id_ticket).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    # Verificar se o ticket é do tipo TROCA
    if ticket.tipo != "TROCA":
        raise HTTPException(status_code=400, detail="Ticket não é do tipo TROCA")
    
    db_troca = SolicitacaoTroca(**troca.dict())
    db.add(db_troca)
    db.commit()
    db.refresh(db_troca)
    return db_troca

@router.get("/trocas/", response_model=List[SolicitacaoTrocaResponse])
def listar_solicitacoes_troca(
    skip: int = 0,
    limit: int = 100,
    status_troca: Optional[str] = None,
    ticket_id: Optional[int] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Lista solicitações de troca com filtros"""
    query = db.query(SolicitacaoTroca)
    
    if status_troca:
        query = query.filter(SolicitacaoTroca.status == status_troca)
    if ticket_id:
        query = query.filter(SolicitacaoTroca.id_ticket == ticket_id)
    if data_inicio:
        query = query.filter(SolicitacaoTroca.data_solicitacao >= data_inicio)
    if data_fim:
        data_fim_completa = datetime.combine(data_fim, datetime.max.time())
        query = query.filter(SolicitacaoTroca.data_solicitacao <= data_fim_completa)
    
    solicitacoes = query.order_by(SolicitacaoTroca.data_solicitacao.desc()).offset(skip).limit(limit).all()
    return solicitacoes

@router.get("/trocas/{troca_id}", response_model=SolicitacaoTrocaResponse)
def obter_solicitacao_troca(troca_id: int, db: Session = Depends(get_db)):
    """Obtém uma solicitação de troca pelo ID"""
    troca = db.query(SolicitacaoTroca).filter(SolicitacaoTroca.id_solicitacao == troca_id).first()
    if not troca:
        raise HTTPException(status_code=404, detail="Solicitação de troca não encontrada")
    return troca

@router.put("/trocas/{troca_id}", response_model=SolicitacaoTrocaResponse)
def atualizar_solicitacao_troca(
    troca_id: int,
    troca_data: SolicitacaoTrocaUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza uma solicitação de troca"""
    troca = db.query(SolicitacaoTroca).filter(SolicitacaoTroca.id_solicitacao == troca_id).first()
    if not troca:
        raise HTTPException(status_code=404, detail="Solicitação de troca não encontrada")
    
    for key, value in troca_data.dict(exclude_unset=True).items():
        setattr(troca, key, value)
    
    db.commit()
    db.refresh(troca)
    return troca

@router.patch("/trocas/{troca_id}/aprovar")
def aprovar_troca(troca_id: int, db: Session = Depends(get_db)):
    """Aprova uma solicitação de troca"""
    return atualizar_status_troca(troca_id, "APROVADA", db)

@router.patch("/trocas/{troca_id}/rejeitar")
def rejeitar_troca(troca_id: int, motivo: str, db: Session = Depends(get_db)):
    """Rejeita uma solicitação de troca"""
    troca = db.query(SolicitacaoTroca).filter(SolicitacaoTroca.id_solicitacao == troca_id).first()
    if not troca:
        raise HTTPException(status_code=404, detail="Solicitação de troca não encontrada")
    
    troca.status = "REJEITADA"
    troca.motivo = f"{troca.motivo or ''} - Rejeitado: {motivo}".strip()
    
    db.commit()
    db.refresh(troca)
    return troca

def atualizar_status_troca(troca_id: int, status: str, db: Session):
    """Função auxiliar para atualizar status da troca"""
    troca = db.query(SolicitacaoTroca).filter(SolicitacaoTroca.id_solicitacao == troca_id).first()
    if not troca:
        raise HTTPException(status_code=404, detail="Solicitação de troca não encontrada")
    
    troca.status = status
    db.commit()
    db.refresh(troca)
    return troca

# ========== VIEWS E RELATÓRIOS ==========
@router.get("/dashboard", response_model=DashboardServicosResponse)
def obter_dashboard(db: Session = Depends(get_db)):
    """Obtém dados para o dashboard de serviços"""
    dashboard = db.query(VwDashboardServicos).first()
    if not dashboard:
        # Se a view não retornar dados, criar um objeto vazio
        dashboard = VwDashboardServicos(
            tickets_abertos=0,
            tickets_hoje=0,
            trocas_pendentes=0,
            total_atendentes=0,
            tempo_medio_resolucao_30_dias=0
        )
    return dashboard

@router.get("/tickets-abertos", response_model=List[TicketAbertoResponse])
def listar_tickets_abertos(
    prioridade: Optional[str] = None,
    tipo: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista todos os tickets abertos"""
    query = db.query(VwTicketsAbertos)
    
    if prioridade:
        query = query.filter(VwTicketsAbertos.prioridade == prioridade)
    if tipo:
        query = query.filter(VwTicketsAbertos.tipo == tipo)
    
    tickets = query.order_by(
        # Ordenar por prioridade (URGENTE primeiro)
        VwTicketsAbertos.prioridade,
        VwTicketsAbertos.data_abertura
    ).all()
    
    return tickets

@router.get("/trocas-pendentes", response_model=List[TrocaPendenteResponse])
def listar_trocas_pendentes(db: Session = Depends(get_db)):
    """Lista todas as trocas pendentes"""
    trocas = db.query(VwTrocasPendentes).all()
    return trocas

@router.get("/historico-cliente/{cliente_id}", response_model=HistoricoClienteResponse)
def obter_historico_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtém o histórico de atendimento de um cliente"""
    historico = db.query(VwHistoricoCliente).filter(
        VwHistoricoCliente.cliente_finalid == cliente_id
    ).first()
    
    if not historico:
        # Se o cliente não tem histórico, verificar se existe
        from models.vc_cliente_final_model import ClienteFinal
        cliente = db.query(ClienteFinal).filter(ClienteFinal.cliente_finalid == cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        # Retornar histórico vazio
        historico = VwHistoricoCliente(
            cliente_finalid=cliente_id,
            cliente=cliente.nome,
            data_ultima_compra=cliente.data_ultima_compra,
            total_tickets=0,
            tickets_resolvidos=0,
            solicitacoes_troca=0,
            solicitacoes_garantia=0,
            ultimo_ticket=None
        )
    
    return historico

@router.get("/metricas-mensais", response_model=List[MetricasMensaisResponse])
def listar_metricas_mensais(
    ano: Optional[int] = None,
    meses: Optional[int] = 12,  # Últimos N meses
    db: Session = Depends(get_db)
):
    """Obtém métricas mensais de atendimento"""
    query = db.query(VwMetricasMensais)
    
    if ano:
        query = query.filter(VwMetricasMensais.ano == ano)
    
    metricas = query.order_by(VwMetricasMensais.mes.desc()).limit(meses).all()
    return metricas

@router.get("/analise-tipos", response_model=List[AnaliseTiposAtendimentoResponse])
def analise_tipos_atendimento(db: Session = Depends(get_db)):
    """Análise de tipos de atendimento"""
    analise = db.query(VwAnaliseTiposAtendimento).all()
    return analise

@router.get("/tempo-resolucao", response_model=List[TempoResolucaoResponse])
def tempo_medio_resolucao(db: Session = Depends(get_db)):
    """Tempo médio de resolução por prioridade"""
    tempos = db.query(VwTempoResolucao).all()
    return tempos

@router.get("/performance-atendentes", response_model=List[PerformanceAtendentesResponse])
def performance_atendentes(db: Session = Depends(get_db)):
    """Performance dos atendentes"""
    performance = db.query(VwPerformanceAtendentes).all()
    return performance

# ========== RELATÓRIOS PERSONALIZADOS ==========
@router.get("/relatorios/tickets-por-cliente")
def relatorio_tickets_por_cliente(
    top_n: int = 10,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Relatório de tickets por cliente"""
    from models.vc_cliente_final_model import ClienteFinal
    
    query = db.query(
        ClienteFinal.cliente_finalid,
        ClienteFinal.nome,
        func.count(TicketAtendimento.id_ticket).label("total_tickets"),
        func.sum(
            case(
                [(TicketAtendimento.status == "RESOLVIDO", 1)],
                else_=0
            )
        ).label("tickets_resolvidos"),
        func.max(TicketAtendimento.data_abertura).label("ultimo_ticket")
    ).join(
        TicketAtendimento, 
        ClienteFinal.cliente_finalid == TicketAtendimento.id_cliente_final,
        isouter=True
    )
    
    if data_inicio:
        query = query.filter(TicketAtendimento.data_abertura >= data_inicio)
    if data_fim:
        data_fim_completa = datetime.combine(data_fim, datetime.max.time())
        query = query.filter(TicketAtendimento.data_abertura <= data_fim_completa)
    
    resultados = query.group_by(
        ClienteFinal.cliente_finalid,
        ClienteFinal.nome
    ).order_by(
        func.count(TicketAtendimento.id_ticket).desc()
    ).limit(top_n).all()
    
    return [
        {
            "cliente_id": r.cliente_finalid,
            "cliente_nome": r.nome,
            "total_tickets": r.total_tickets or 0,
            "tickets_resolvidos": r.tickets_resolvidos or 0,
            "taxa_resolucao": round((r.tickets_resolvidos or 0) / (r.total_tickets or 1) * 100, 2) if r.total_tickets else 0,
            "ultimo_ticket": r.ultimo_ticket
        }
        for r in resultados
    ]

@router.get("/relatorios/evolucao-diaria")
def evolucao_diaria_tickets(
    dias: int = 30,
    db: Session = Depends(get_db)
):
    """Evolução diária de tickets (últimos N dias)"""
    data_inicio = date.today() - timedelta(days=dias)
    
    resultados = db.query(
        func.date(TicketAtendimento.data_abertura).label("data"),
        func.count(TicketAtendimento.id_ticket).label("total_tickets"),
        func.count(
            case(
                [(TicketAtendimento.status == "RESOLVIDO", 1)],
                else_=0
            )
        ).label("tickets_resolvidos")
    ).filter(
        TicketAtendimento.data_abertura >= data_inicio
    ).group_by(
        func.date(TicketAtendimento.data_abertura)
    ).order_by(
        func.date(TicketAtendimento.data_abertura).desc()
    ).all()
    
    return [
        {
            "data": r.data,
            "total_tickets": r.total_tickets,
            "tickets_resolvidos": r.tickets_resolvidos,
            "taxa_resolucao": round(r.tickets_resolvidos / r.total_tickets * 100, 2) if r.total_tickets > 0 else 0
        }
        for r in resultados
    ]

@router.get("/relatorios/tickets-por-setor")
def tickets_por_setor(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Relatório de tickets por setor (baseado em tipos)"""
    query = db.query(
        TicketAtendimento.tipo,
        func.count(TicketAtendimento.id_ticket).label("total_tickets"),
        func.avg(
            func.extract('epoch', TicketAtendimento.data_resolucao - TicketAtendimento.data_abertura) / 3600
        ).label("tempo_medio_horas")
    ).filter(
        TicketAtendimento.tipo.isnot(None)
    )
    
    if data_inicio:
        query = query.filter(TicketAtendimento.data_abertura >= data_inicio)
    if data_fim:
        data_fim_completa = datetime.combine(data_fim, datetime.max.time())
        query = query.filter(TicketAtendimento.data_abertura <= data_fim_completa)
    
    resultados = query.group_by(
        TicketAtendimento.tipo
    ).order_by(
        func.count(TicketAtendimento.id_ticket).desc()
    ).all()
    
    return [
        {
            "tipo": r.tipo,
            "total_tickets": r.total_tickets,
            "tempo_medio_horas": round(float(r.tempo_medio_horas or 0), 2)
        }
        for r in resultados
    ]

# ========== ENDPOINTS ÚTEIS ==========
@router.get("/clientes/{cliente_id}/tickets", response_model=List[TicketAtendimentoResponse])
def obter_tickets_cliente(
    cliente_id: int,
    status: Optional[str] = None,
    tipo: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtém todos os tickets de um cliente específico"""
    query = db.query(TicketAtendimento).filter(
        TicketAtendimento.id_cliente_final == cliente_id
    )
    
    if status:
        query = query.filter(TicketAtendimento.status == status)
    if tipo:
        query = query.filter(TicketAtendimento.tipo == tipo)
    
    tickets = query.order_by(TicketAtendimento.data_abertura.desc()).all()
    return tickets

@router.get("/pedidos/{pedido_id}/tickets", response_model=List[TicketAtendimentoResponse])
def obter_tickets_pedido(pedido_id: int, db: Session = Depends(get_db)):
    """Obtém todos os tickets relacionados a um pedido"""
    tickets = db.query(TicketAtendimento).filter(
        TicketAtendimento.id_pedido == pedido_id
    ).order_by(TicketAtendimento.data_abertura.desc()).all()
    
    return tickets

@router.get("/tickets/{ticket_id}/trocas", response_model=List[SolicitacaoTrocaResponse])
def obter_trocas_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Obtém todas as solicitações de troca de um ticket"""
    # Verificar se o ticket existe
    ticket = db.query(TicketAtendimento).filter(TicketAtendimento.id_ticket == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    trocas = db.query(SolicitacaoTroca).filter(
        SolicitacaoTroca.id_ticket == ticket_id
    ).order_by(SolicitacaoTroca.data_solicitacao.desc()).all()
    
    return trocas

# ========== ESTATÍSTICAS RÁPIDAS ==========
@router.get("/estatisticas/gerais")
def estatisticas_gerais(db: Session = Depends(get_db)):
    """Estatísticas gerais do módulo SM"""
    # Total de tickets
    total_tickets = db.query(func.count(TicketAtendimento.id_ticket)).scalar() or 0
    
    # Tickets abertos
    tickets_abertos = db.query(func.count(TicketAtendimento.id_ticket)).filter(
        TicketAtendimento.status.in_(["ABERTO", "EM_ANDAMENTO"])
    ).scalar() or 0
    
    # Tickets resolvidos hoje
    hoje = date.today()
    tickets_hoje = db.query(func.count(TicketAtendimento.id_ticket)).filter(
        func.date(TicketAtendimento.data_abertura) == hoje
    ).scalar() or 0
    
    # Trocas pendentes
    trocas_pendentes = db.query(func.count(SolicitacaoTroca.id_solicitacao)).filter(
        SolicitacaoTroca.status.in_(["SOLICITADA", "EM_ANALISE"])
    ).scalar() or 0
    
    # Atendentes ativos
    total_atendentes = db.query(func.count(Atendente.id_atendente)).scalar() or 0
    
    # Ticket mais antigo aberto
    ticket_mais_antigo = db.query(TicketAtendimento).filter(
        TicketAtendimento.status.in_(["ABERTO", "EM_ANDAMENTO"])
    ).order_by(TicketAtendimento.data_abertura.asc()).first()
    
    return {
        "total_tickets": total_tickets,
        "tickets_abertos": tickets_abertos,
        "tickets_hoje": tickets_hoje,
        "trocas_pendentes": trocas_pendentes,
        "total_atendentes": total_atendentes,
        "taxa_tickets_abertos": round((tickets_abertos / total_tickets * 100), 2) if total_tickets > 0 else 0,
        "ticket_mais_antigo": {
            "id": ticket_mais_antigo.id_ticket if ticket_mais_antigo else None,
            "data_abertura": ticket_mais_antigo.data_abertura if ticket_mais_antigo else None,
            "assunto": ticket_mais_antigo.assunto if ticket_mais_antigo else None
        }
    }