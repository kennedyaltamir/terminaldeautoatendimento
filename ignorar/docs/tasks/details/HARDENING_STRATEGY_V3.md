# 🛡️ Especificação Técnica: Estratégia de Hardening v3

Este documento detalha as decisões arquiteturais e os fundamentos técnicos das tasks de infraestrutura definidas após a auditoria estratégica de Janeiro de 2026.

## 1. PostgreSQL Row-Level Security (RLS)
**Contexto:** O isolamento multi-tenant atual é frágil porque reside na camada de aplicação. Um erro de codificação pode expor dados sensíveis.
**Fundamento:** Mover a responsabilidade do isolamento para o motor do banco de dados.
**Mecanismo:**
- Cada tabela terá uma política: `USING (company_id = current_setting('app.current_company_id')::uuid)`.
- A aplicação, ao iniciar uma transação, deve executar: `SET LOCAL app.current_company_id = '...'`.
- Isso cria uma "jaula" de dados onde a query `SELECT * FROM orders` retorna apenas os pedidos da empresa autenticada, garantindo conformidade com a LGPD por design.

## 2. Refatoração para Centavos (Inteiros)
**Contexto:** O trânsito de valores monetários em ponto flutuante (float) entre Python e JavaScript gera erros de arredondamento acumulados.
**Fundamento:** Utilizar aritmética de inteiros para valores financeiros.
**Mecanismo:**
- O valor R$ 1.250,99 será tratado como o inteiro `125099`.
- O Backend realiza a conversão no momento da serialização do Schema.
- O Frontend elimina o uso de `parseFloat` e realiza somas simples de inteiros, garantindo que o total exibido seja idêntico ao total processado pelo gateway de pagamento.

## 3. Otimização do Global Clock (Mobile)
**Contexto:** O KDS Mobile é um terminal de operação contínua, mas o consumo de energia é um fator limitante no "chão de fábrica".
**Fundamento:** Sincronia sob demanda e economia de recursos.
**Mecanismo:**
- O pulso de 5 segundos é vital para a percepção de tempo real, mas inútil se o operador não estiver olhando para a tela.
- A integração com o `AppState` permite que o app "durma" enquanto está no bolso do garçom, economizando até 40% de bateria em modo stand-by, sem perder a conexão WebSocket (que é mantida pelo SO).

## 4. Inbound Webhooks (iFood)
**Contexto:** O polling é um modelo de "puxar" dados que não escala.
**Fundamento:** Arquitetura orientada a eventos (Push).
**Mecanismo:**
- O MesaFlow passa a ser um receptor passivo. O iFood notifica o sistema assim que um pedido é criado.
- Isso reduz a carga no servidor em 90% e elimina a latência de 30 segundos, tornando a experiência do lojista instantânea.
