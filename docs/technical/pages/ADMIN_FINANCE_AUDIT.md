# 💰 Tela: Auditoria Financeira & Ledger
**Rota:** `/admin/[slug]/audit/financial`
**Domínio:** ADMIN / FINTECH

## 1. Especificação Visual
- **Status de Integridade:** Banner verde/vermelho indicando se a Hash Chain está íntegra.
- **Tabela de Ledger:** Lista imutável de transações (ID, Tipo, Valor, Hash, Referência).
- **Painel de Conciliação:** Comparativo entre "Sistema" vs "Gateway (Mercado Pago)".

## 2. Elementos Interagíveis
- **Botão "Verificar Cadeia":** Dispara script de re-hashing de todas as transações.
- **Botão "Corrigir Órfão":** Cria entrada corretiva no Ledger para transações detectadas apenas no Gateway.

## 3. Comportamento Esperado
- **Imutabilidade:** Esta tela não permite DELETE ou UPDATE. Apenas visualização e inserção de "Entradas de Ajuste".
- **Alerta de Violação:** Se o hash calculado divergir do gravado, a tela deve entrar em modo de alerta crítico.

## 4. APIs Consumidas
- `GET /api/admin/audit/financial/ledger`: Histórico de entradas.
- `GET /api/admin/audit/financial/reconciliation`: Relatório de divergências.
- `POST /api/admin/audit/financial/verify-integrity`: Trigger de auditoria.
