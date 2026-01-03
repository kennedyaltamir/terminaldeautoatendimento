
### 3️⃣ `docs/ARCHITECTURE.md` (Com Justificativa Monolito)

Adicionei a seção de decisão técnica crítica.

```markdown
# 🏗️ Arquitetura do Sistema

## 1. Diagrama de Componentes

```text
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  Cliente     │       │   API Gateway│       │  Banco de    │
│ (Mobile Web) │ ────► │  (FastAPI)   │ ────► │    Dados     │
└──────────────┘       └──────┬───────┘       │ (PostgreSQL) │
                              │               └──────────────┘
┌──────────────┐              │
│   Admin/KDS  │ ◄────────────┘
│  (Desktop)   │
└──────────────┘
```

## 2. Decisões de Design (ADR)

### 🏛️ Por que Monolito Modular?
Optamos por **não usar microserviços** nesta fase pelos seguintes motivos:
1.  **Complexidade Operacional:** Gerenciar 1 container é mais barato e simples que orquestrar 10 serviços no Kubernetes.
2.  **Latência:** Comunicação em memória é mais rápida que chamadas HTTP entre serviços.
3.  **Consistência:** Transações de banco de dados (ACID) são triviais no monolito e complexas em sistemas distribuídos.
4.  **Evolução:** O código está organizado em módulos (`orders`, `products`, `auth`). Se um dia precisarmos separar, o desacoplamento lógico já existe.

### 🔐 Estratégia Multi-tenant
Utilizamos **Isolamento Lógico (Row-Level)**.
*   Todas as empresas compartilham o mesmo banco e tabelas.
*   Toda query obrigatoriamente filtra por `company_id`.
*   **Motivo:** Custo-benefício. Criar um banco por cliente (Isolamento Físico) seria inviável financeiramente para o plano Free.
```
