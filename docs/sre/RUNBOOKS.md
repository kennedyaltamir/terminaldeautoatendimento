
# 🛠️ Runbooks Operacionais (SRE)

## RB-001: Falha de Banco de Dados (Neon)
**Sintoma:** Erros 500 persistentes com log `OperationalError`.
1. Verifique o status em `neon.tech/status`.
2. Se a região estiver offline, acione o script de failover para réplica de leitura (se disponível).
3. Notifique clientes via Status Page (Trust Center).

## RB-002: Queda do Redis
**Sintoma:** KDS não atualiza em tempo real.
1. O sistema deve entrar em fallback automático.
2. Verifique se a variável `REDIS_URL` está correta.
3. Reinicie o cluster Redis via painel do provedor.

## RB-003: SLO Breach / Circuit Breaker Aberto
**Sintoma:** API retornando 503 para 100% das requisições.
1. Identifique a causa do erro (ex: latência externa de pagamento).
2. Se a causa for mitigada, aguarde o estado `HALF_OPEN` (30s).
3. **Manual Override:** Se necessário forçar o fechamento, execute:
   `redis-cli set cb:state CLOSED`

## RB-004: Conflito de Idempotência
**Sintoma:** Cliente reclama de cobrança mas pedido não aparece.
1. Consulte a tabela `payment_transactions` pelo ID externo.
2. Verifique se o evento foi processado mas a notificação falhou.
3. Execute o re-processamento manual do webhook.

