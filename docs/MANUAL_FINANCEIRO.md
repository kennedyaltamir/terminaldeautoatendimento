# 💰 Manual do Motor Financeiro MesaFlow

Este documento detalha a operação, configuração e fluxo de caixa das funcionalidades financeiras do sistema. O MesaFlow foi desenhado para ser uma **Fintech Embutida**, gerando receita tanto para o restaurante quanto para a plataforma (SaaS).

---

## 1. Split de Pagamento (Comissão Automática)

O Split é a funcionalidade que permite ao MesaFlow cobrar uma taxa (comissão) sobre cada transação Pix realizada, retendo o valor na fonte antes que ele chegue ao restaurante.

### 🔄 Como Funciona o Fluxo
1.  **Venda:** O cliente faz um pedido de **R$ 100,00**.
2.  **Processamento:** O sistema gera um QR Code Pix via Mercado Pago.
3.  **Divisão (Split):** No momento do pagamento, o Mercado Pago lê a regra de comissão (ex: 2%).
4.  **Liquidação Instantânea:**
    *   **R$ 98,00** vão para a conta do **Restaurante**.
    *   **R$ 2,00** vão para a conta do **MesaFlow (SaaS)**.

### ⚙️ Configuração Técnica
A taxa é definida individualmente por estabelecimento no banco de dados. Isso permite negociações flexíveis (ex: taxas menores para grandes redes).

**Requisitos:**
*   Token de Produção do Mercado Pago (`APP_USR-...`) configurado na conta do SaaS.

**Comando SQL para definir taxa:**
```sql
-- Define 2.5% de comissão para a Hamburgueria do Zé
UPDATE companies 
SET marketplace_fee_percentage = 2.50 
WHERE slug = 'hamburgueria-ze';
2. Cobrança de Vendas Offline (Dinheiro/Cartão Físico)
Como o MesaFlow não toca no dinheiro físico, a taxa de comissão (ex: 2,5%) funciona no modelo Pós-Pago (Ledger).
🔄 Fluxo de Acúmulo e Cobrança
Venda: O garçom fecha uma mesa de R$ 100,00 em Dinheiro.
Cálculo: O sistema calcula a taxa (R$ 2,50) e adiciona ao saldo devedor da empresa (pending_commission_balance).
Faturamento: O valor acumulado das comissões será somado automaticamente à próxima fatura de assinatura do sistema (cobrada no cartão de crédito cadastrado no Stripe).
Transparência: O dono pode ver o saldo acumulado de comissões pendentes no Dashboard Financeiro.
3. Planos de Assinatura (SaaS)
O sistema possui um motor de cobrança recorrente integrado ao Stripe. O acesso a recursos avançados é controlado automaticamente pelo status do pagamento.
📦 Estrutura de Planos
Recurso	Plano Start (Grátis)	Plano Pro (R$ 149/mês)
Limite de Pedidos	50 / mês	Ilimitado
Limite de Produtos	15 itens	Ilimitado
KDS (Cozinha)	❌ Bloqueado	✅ Liberado
Gestão de Estoque	❌ Bloqueado	✅ Liberado
App do Garçom	❌ Bloqueado	✅ Liberado
Fidelidade	❌ Bloqueado	✅ Liberado
🔄 Ciclo de Vida da Assinatura
Contratação: O dono clica em "Assinar Agora" no painel -> Paga no Checkout do Stripe.
Ativação: O sistema recebe um Webhook (checkout.session.completed) e libera os recursos instantaneamente.
Gestão: O dono pode acessar o "Portal do Cliente" para trocar o cartão ou baixar faturas.
Inadimplência/Cancelamento: Se o pagamento falhar ou for cancelado, o sistema recebe o evento (customer.subscription.deleted) e reverte a conta para o plano Start, bloqueando o acesso ao KDS e novos produtos.
4. Sistema de Fidelidade (Cashback)
Uma ferramenta de retenção automática que incentiva o cliente a voltar.
🎯 Lógica do Cashback
Acúmulo: O dono define uma porcentagem (ex: 5%). Se o cliente gastar R
100
,
00
,
e
l
e
g
a
n
h
a
R
100,00,eleganhaR
 5,00 de crédito.
Identificação: O saldo é vinculado ao número de telefone do cliente.
Resgate: No próximo pedido, se o cliente informar o mesmo telefone, o carrinho exibe um widget: "Você tem R$ 5,00 de saldo. Usar agora?".
Regra de Negócio: O cashback é calculado apenas sobre o valor efetivamente pago em dinheiro/cartão (o valor abatido por saldo não gera novo cashback).
5. Dashboard Financeiro
O painel administrativo oferece métricas em tempo real, calculadas diretamente do banco de dados para garantir precisão.
📊 Indicadores Disponíveis
Faturamento Bruto: Total de vendas pagas no período.
Ticket Médio: Valor médio gasto por pedido.
Vendas por Hora (Heatmap): Gráfico de barras mostrando os horários de pico.
Curva ABC (Top Produtos): Ranking dos itens que mais geram receita.
Exportação: Botão para baixar relatório detalhado em CSV (compatível com Excel).
code
Code
# tests/test_offline_fee.py
```python
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Company, Table, TableSession, Order, OrderStatus, PaymentStatus
from decimal import Decimal
import uuid

client = TestClient(app)

def test_offline_fee_accumulation():
    """
    Testa se a comissão de vendas em dinheiro é acumulada corretamente no saldo devedor da empresa.
    """
    # 1. Setup
    unique_slug = f"fee-test-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Fee Corp",
        slug=unique_slug,
        owner_email=f"fee-{uuid.uuid4().hex[:6]}@test.com",
        marketplace_fee_percentage=Decimal("2.50"), # 2.5% de taxa
        pending_commission_balance=Decimal("0.00")
    )
    db.add(company)
    db.commit()
    
    # Criar Mesa e Sessão
    table = Table(company_id=company.id, table_number=1, qr_token="token")
    db.add(table)
    db.commit()
    
    session = TableSession(
        company_id=company.id, table_id=table.id, customer_name="Fee Payer",
        session_token="sess_fee", access_pin="0000", is_active=True
    )
    db.add(session)
    db.commit()
    
    # Criar Pedido de R$ 100.00
    order = Order(
        company_id=company.id, session_id=session.id, table_id=table.id,
        total_amount=Decimal("100.00"), status=OrderStatus.PENDING
    )
    db.add(order)
    db.commit()
    
    company_id = company.id
    table_id = table.id
    
    # Token Admin
    from app.core.security import create_access_token
    token = create_access_token(data={"sub": company.owner_email, "role": "owner", "account_type": "company"})
    headers = {"Authorization": f"Bearer {token}"}
    
    db.close()

    # 2. Fechar Mesa com Dinheiro
    res = client.post(
        f"/api/admin/tables/{table_id}/close",
        headers=headers,
        json={"payment_method": "cash"}
    )
    assert res.status_code == 200

    # 3. Verificar Saldo Devedor
    db = SessionLocal()
    updated_company = db.query(Company).filter(Company.id == company_id).first()
    
    # 2.5% de 100 = 2.50
    assert updated_company.pending_commission_balance == Decimal("2.50")
    
    db.close()
Comandos para Execução
code
Bash
python atualizar.py
python -m pytest tests/test_offline_fee.py
info
Google AI models may make mistakes, so double-check outputs.
Use Arrow Up and Arrow Down to select a turn, Enter to jump to it, and Escape to return to the chat.
