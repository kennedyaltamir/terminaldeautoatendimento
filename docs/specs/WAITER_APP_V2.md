# 📱 Especificação Técnica: Garçom Pro (Mobile POS v2)

**Objetivo:** Transformar o aplicativo do garçom de um simples "anotador de pedidos" em uma ferramenta de vendas e gestão de relacionamento (CRM).

---

## 1. Identificação de Cliente (CRM na Ponta)
Ao abrir uma mesa, o garçom deve ser capaz de identificar o cliente para personalizar o atendimento.

### Fluxo de UI
1.  Garçom clica em "Abrir Mesa".
2.  Input: "Telefone do Cliente (Opcional)".
3.  **Ação:** Ao digitar, o sistema consulta a API `/api/{slug}/wallet/{phone}`.
4.  **Feedback Visual:**
    *   Se cliente existe: Mostra "Nome: João", "Saldo Cashback: R$ 15,00", "Última visita: 3 dias atrás".
    *   Se novo: "Novo Cliente (Será cadastrado)".

### Integração Backend
*   **Endpoint:** `GET /api/{slug}/wallet/{phone}`
*   **Uso:** Exibir saldo de cashback disponível para abater na conta imediatamente.

---

## 2. Sugestão Inteligente (IA na Ponta)
O garçom deve atuar como um consultor, sugerindo itens que combinam.

### Fluxo de UI
1.  Garçom adiciona "Hambúrguer" ao carrinho.
2.  **Ação:** O sistema consulta as recomendações do produto (`product.recommendations`).
3.  **Feedback Visual:** Um *toast* ou *bottom sheet* discreto aparece:
    *   "💡 Sugira: Batata Frita (+ R$ 10,00) ou Coca-Cola".
4.  **Botão Rápido:** Um toque no item sugerido adiciona ao pedido sem abrir modal.

### Integração Backend
*   **Fonte de Dados:** O campo `recommendations` já vem populado no endpoint `GET /menu` e `GET /products`.
*   **Lógica:** Frontend deve filtrar recomendações para não sugerir o que já está no carrinho.

---

## 3. Split de Conta por Item
Resolver o problema de "Eu só comi uma salada e bebi uma água".

### Fluxo de UI (Modal de Pagamento)
1.  Garçom clica em "Fechar Conta".
2.  Opção: "Dividir por Item".
3.  **Interface:** Lista de todos os itens da mesa com checkboxes.
4.  **Ação:** Garçom seleciona "1x Salada" e "1x Água".
5.  **Cálculo:** O sistema soma apenas esses itens (+ 10% proporcional).
6.  **Pagamento:** Realiza o pagamento parcial.
7.  **Estado:** Os itens pagos ficam "ticados" visualmente (apenas no front) ou o valor total da mesa é reduzido.

### Integração Backend
*   **Estratégia:** Pagamento Parcial.
*   O backend não precisa saber *quais* itens foram pagos, apenas o *valor*.
*   Se a mesa deve R$ 200,00 e o cliente paga R$ 40,00 (referente à salada), o backend registra um pagamento de R$ 40,00 e o saldo devedor cai para R$ 160,00.

---

## 4. Gestão de Gorjeta (Taxa de Serviço)
Flexibilidade para negociar a taxa de serviço na hora do pagamento.

### Fluxo de UI
1.  Tela de Fechamento.
2.  Exibição: "Serviço (10%): R$ 25,00".
3.  **Ação:** Botão "Editar".
4.  **Opções:**
    *   Remover (0%).
    *   Alterar % (ex: 15% ou 5%).
    *   Valor Fixo (ex: R$ 10,00).
5.  **Recálculo:** O total final é atualizado.

### Integração Backend
*   **Endpoint:** `POST /api/admin/tables/{id}/close`
*   **Novo Campo:** `custom_service_fee` (Decimal) ou `service_fee_percent` (Decimal).
*   **Lógica:** Se enviado, o backend usa este valor para o `ServiceFeeLedger` em vez do padrão da empresa.

---

## 5. Cenários de Teste (QA)

| ID | Cenário | Resultado Esperado |
|:---|:---|:---|
| **GP-01** | Identificar cliente com saldo | Mostrar saldo e botão "Usar Saldo". |
| **GP-02** | Adicionar produto com IA | Exibir sugestão correta baseada no histórico. |
| **GP-03** | Fechar conta removendo 10% | Total deve ser igual à soma dos produtos. Ledger de gorjeta = 0. |
| **GP-04** | Fechar conta com 15% | Total deve incluir 15%. Ledger deve registrar valor maior. |
