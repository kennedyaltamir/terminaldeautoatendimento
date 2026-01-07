🚨 Plano de Resposta a Incidentes

Objetivo: Restaurar o serviço o mais rápido possível e comunicar com transparência.

1. Níveis de Severidade
Nível	Descrição	Exemplo	Tempo de Resposta
SEV1 (Crítico)	Sistema fora do ar. Perda de receita.	Banco caiu, DNS falhou.	Imediato (Acordar equipe)
SEV2 (Alto)	Funcionalidade core quebrada.	Pix não gera, KDS não toca som.	< 30 min
SEV3 (Médio)	Funcionalidade secundária ou lentidão.	Relatórios lentos, erro de CSS.	< 4 horas
SEV4 (Baixo)	Bug visual ou dúvida.	Typos, cor errada.	Próxima Sprint
2. Papéis na Crise

Comandante do Incidente (IC): (Geralmente o CTO). Toma as decisões, não toca no código.

Operador: (DevOps/Backend Lead). Executa os comandos e correções.

Comunicação: (CS/Product). Fala com os clientes e atualiza a Status Page.

3. Fluxo de Resposta (SEV1/SEV2)

Detecção: Alerta do Sentry/UptimeRobot ou chamado de cliente.

Reconhecimento: IC declara o incidente no canal #war-room do Slack/Discord.

Contenção:

Reverter o último deploy (git revert).

Ativar modo de manutenção se necessário.

Comunicação:

Atualizar Status Page: "Estamos investigando uma instabilidade..."

Enviar template de WhatsApp para clientes Enterprise.

Resolução: Aplicar fix.

Post-Mortem: Em até 24h, documentar a causa raiz e criar tarefas para evitar recorrência.

4. Templates de Comunicação

Status Page (Investigando):

"Identificamos uma instabilidade no processamento de pedidos. Nossa equipe de engenharia já está atuando. Próxima atualização em 15 min."

Status Page (Resolvido):

"O serviço foi restabelecido. A causa foi identificada (falha no provedor de banco de dados) e mitigada. Todos os sistemas operam normalmente."
