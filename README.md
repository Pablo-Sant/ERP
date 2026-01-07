# 🏢 BluERP - Engenharia de Software e Gestão Integrada

O **BluERP** é uma plataforma de gestão empresarial desenhada para centralizar operações e otimizar o fluxo de informações entre departamentos. O projeto foca na construção de uma API de alta performance, capaz de sustentar processos de negócio complexos através de uma estrutura modular e escalável.

## 💼 Arquitetura de Negócio
O sistema foi projetado para atuar como o núcleo operacional de uma organização, integrando fluxos de trabalho que vão desde a gestão de pessoas até a análise estratégica de dados:

* **Vendas e Compras:** Ciclo completo de gestão de clientes e contratos.
* **Financeiro:** Gestão de contas a pagar/receber e planejamento orçamentário.
* **Recursos Humanos:** Controle de colaboradores e estruturas organizacionais.
* **Gestão de Materiais e Ativos:** Rastreabilidade de estoque, patrimônio e suprimentos.
* **Gestão de Projetos:** Planejamento e monitoramento de cronogramas e execução.
* **Business Intelligence:** Camada de analytics para transformação de dados em relatórios estratégicos.
* **Serviços:** Gestão de atendimento e suporte ao cliente.

## 🏗️ Decisões de Engenharia
A construção do backend prioriza a manutenção e a independência entre as camadas do sistema:

* **Modularização:** Organização do projeto em diretórios específicos para `api`, `models`, `schemas` e `services`, garantindo a separação de responsabilidades.
* **Lógica de Domínio:** Isolamento das regras de negócio na camada de `services`, mantendo as rotas da API focadas apenas na orquestração das requisições.
* **Integridade de Dados:** Uso de schemas Pydantic para validação rigorosa de contratos e models SQLAlchemy para gerenciamento do banco de dados relacional.
* **Segurança de Credenciais:** Implementação de hashing de senhas via Argon2 e autenticação baseada em tokens JWT.
* **Processamento Assíncrono:** Utilização de `AsyncSession` para operações não bloqueantes com o banco de dados PostgreSQL.

## 🛠️ Tecnologias
* **Linguagem:** Python.
* **Framework:** FastAPI.
* **Banco de Dados:** PostgreSQL.
* **ORM:** SQLAlchemy (Async).
* **Segurança:** JWT (JSON Web Tokens) e Argon2.


## ⚡ Quick Start (Como executar)

### Pré-requisitos
* Python 3.10+
* PostgreSQL ativo

### Instalação
1. Clone o repositório: `git clone https://github.com/seu-usuario/bluerp.git`
2. Crie o ambiente virtual: `python -m venv .venv`
3. Ative o venv: `source .venv/bin/activate` (Linux/Mac) ou `.venv\Scripts\activate` (Windows)
4. Instale as dependências: `pip install -r requirements.txt`
5. Configure o `.env` com sua `DATABASE_URL`.
6. Crie as tabelas: `python criar_tabelas.py`
7. Inicie a API: `uvicorn main:app --reload`

📍 Acesse a documentação interativa em: `http://127.0.0.1:8000/docs`

---

## 📊 Status do Projeto e Maturidade
| Recurso | Status | Observação |
| :--- | :--- | :--- |
| **Arquitetura Base** | ✅ Concluído | Estrutura modular (Services/Models/Schemas). |
| **Módulos de Negócio** | ✅ Implementado | Rotas de todos os departamentos (Vendas, RH, Financeiro, etc). |
| **Autenticação** | 🔐 Parcial | JWT e Argon2 implementados; proteção em rotas críticas. |
| **Testes Unitários** | 🏗️ Em progresso | Estrutura de diretórios criada para Pytest. |
| **Deploy/CI-CD** | ⏳ Planejado | Próxima fase do roadmap. |

---