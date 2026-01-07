🔥 Runbook: Falha no Banco de Dados (PostgreSQL/Neon)

Severidade: CRÍTICA (SEV1)
Sintoma: API retorna Erro 500, Logs mostram OperationalError, Connection Refused ou ReadOnly.

1. Diagnóstico Rápido

Acesse o painel do Neon.tech.

Verifique o status do "Compute Endpoint" (Deve estar Active).

Verifique o uso de conexões (Se estiver em 100%, o Pooler travou).

2. Procedimentos de Recuperação
Cenário A: Pool de Conexões Esgotado

Se o erro for too many clients:

No Render, reinicie o serviço mesaflow-api para matar conexões zumbis.

No Neon, verifique se está usando a URL com -pooler. Se não, altere a variável DATABASE_URL no Render imediatamente para usar o PgBouncer.

Cenário B: Banco Travado/Lento

No Neon, vá em Dashboard > Compute.

Clique em Restart Compute. (Downtime estimado: 5-10 segundos).

Cenário C: Corrupção de Dados / Delete Acidental

No Neon, vá em History (Time Travel).

Identifique o horário exato antes do incidente.

Clique em Restore to this point.

Isso criará um novo branch do banco.

Atualize a DATABASE_URL no Render para apontar para este novo branch.

3. Pós-Incidente

Verifique a integridade dos últimos pedidos.

Emita um comunicado de "Incidente Resolvido" na página de status.

Escreva o Post-Mortem.
