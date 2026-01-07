🔥 Runbook: Falha no Redis (WebSockets/KDS)

Severidade: ALTA (SEV2)
Sintoma: KDS não atualiza sozinho, Garçom não recebe alertas, Erros de Connection refused no log do Backend.

1. Impacto

O sistema NÃO PARA. O MesaFlow foi desenhado para degradar graciosamente.

Sem Redis: O backend reverte para memória local (funciona se houver apenas 1 instância da API).

Se houver múltiplas instâncias: A sincronização entre elas falha (KDS pode não tocar se estiver conectado em um worker diferente do que recebeu o pedido).

2. Procedimentos de Recuperação
Passo 1: Verificar Conexão

Acesse o painel do provedor Redis (Upstash ou Render Redis).

Verifique se o limite de memória ou conexões foi atingido.

Passo 2: Reiniciar Serviço

Se for Render Redis: No dashboard, clique em Restart.

Se for Upstash: Verifique se a quota mensal estourou. Se sim, faça upgrade do plano imediatamente.

Passo 3: Modo de Emergência (Polling)

Se o Redis morreu definitivamente e não volta:

No Frontend (frontend/.env), altere NEXT_PUBLIC_USE_POLLING=true (se implementado) ou instrua os clientes a atualizarem a página manualmente (F5).

O KDS possui um botão "Atualizar" manual no topo. Instrua o suporte a avisar os clientes para usá-lo.

3. Validação

Abra o KDS e o Menu em abas diferentes.

Faça um pedido.

Verifique se o KDS atualiza em < 1s.
