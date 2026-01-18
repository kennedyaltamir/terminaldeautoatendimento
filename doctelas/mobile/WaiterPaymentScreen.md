# 💰 WaiterPaymentScreen
> **Plataforma:** MOBILE | **Domínio:** FINTECH | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Interface de checkout móvel que transforma o smartphone do garçom em um terminal de recebimento. Permite processar pagamentos via Pix (dinâmico), Dinheiro (com calculadora de troco) e Cartão, integrando o fluxo financeiro diretamente ao Ledger do sistema.

## 2. Estrutura e Componentes
- **Order Summary Header:** Exibição do total da mesa, taxa de serviço e descontos aplicados.
- **Payment Method Grid:** Seleção intuitiva entre Pix, Dinheiro e Cartão.
- **Dynamic QR Code Area:** Renderização nativa do código Pix gerado pelo gateway.
- **Change Calculator:** Teclado numérico otimizado para cálculo de troco em tempo real.

## 3. Elementos Interativos
- **Generate Pix Button:** Dispara a criação da transação no Mercado Pago/Stripe.
- **Manual Confirmation:** Botão de "Confirmar Recebimento" para validação visual do staff.
- **Tip Adjuster:** Permite alterar o valor da gorjeta antes de gerar o total final.

## 4. Regras de Negócio (Fintech)
- **Idempotency Lock:** Impede a geração de múltiplos QR Codes para a mesma tentativa de pagamento.
- **Ledger Entry:** Cada confirmação de pagamento cria um registro imutável no `FinancialLedger` com hash de integridade.
- **Split Logic:** Aplica automaticamente a retenção de comissão da plataforma conforme configurado no Tenant.

## 5. Estados da Tela
- **Processing:** Overlay de carregamento durante a comunicação com o gateway de pagamento.
- **Success Animation:** Feedback visual e tátil (vibration) após a confirmação do pagamento.
- **Payment Failed:** Diagnóstico de erro amigável com opção de troca de método de pagamento.

## 6. Integração Técnica
- **Endpoints:**
  - `POST /api/admin/tables/{id}/close`
  - `POST /api/admin/tables/{id}/pay`
- **Security:** Exige token JWT válido com permissão de `cashier` ou superior.

---
*MesaFlow Fintech Kernel v5.0*
# 💰 WaiterPaymentScreen
> **Plataforma:** MOBILE | **Domínio:** FINTECH | **Status:** SEALED (100%)

## 1. Visão Geral e Propósito
Terminal de recebimento móvel. Permite o fechamento de contas na mesa com Pix dinâmico.

## 2. Estrutura e Layout (Componentes)
- **Totalizer:** Valor final com taxas.
- **Method Grid:** Seleção de Pix, Dinheiro ou Cartão.

## 3. Interações e Ações (Botões)
- **Generate Pix:** Cria transação no gateway.
- **Confirm Cash:** Baixa manual.

## 4. Estados e Cenários (Loading/Error)
- **Waiting Payment:** Exibição do QR Code.
- **Confirmed:** Animação de sucesso.

## 5. Fluxo de Navegação
1. Seleção de método.
2. Processamento.
3. Finalização.

## 6. Documentação Técnica (API)
- **Endpoints:** `POST /api/admin/tables/{id}/close`
- **Assets:** ![Payment Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/mobile-pay-full.png)
