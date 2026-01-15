# DOMAIN: BACKEND
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-ESC-01
TITLE: Migrar Integração iFood para Inbound Webhooks
OWNER: Executor Kernel
PRIORITY: ALTA
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- A integração atual com o iFood utiliza um serviço de polling (`app/services/ifood_service.py`) que consulta a API externa a cada 30 segundos para cada restaurante cadastrado.
- Este modelo gera saturação de I/O de rede e desperdício de conexões com o banco de dados.
- Existe um atraso inerente de até 30 segundos no recebimento de novos pedidos.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Implementação de um endpoint de Webhook (`POST /api/webhooks/ifood`) para recepção passiva de eventos.
- O sistema processa eventos `PLACED`, `CONFIRMED` e `CANCELLED` em tempo real.
- O serviço de polling é rebaixado para "Fallback Mode", rodando apenas uma vez a cada 15 minutos para garantir que nenhum evento foi perdido por falha de rede.
- Implementação de validação de assinatura HMAC para garantir que as requisições partem do iFood.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Criação da rota de Webhook no FastAPI.
- Lógica de validação de segurança (Signature Validation).
- Refatoração do `IfoodService` para aceitar processamento de evento único.
### EXCLUI
- Alterações na lógica de mapeamento de produtos ou categorias.
- Alterações na interface do KDS.

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Framework: FastAPI.
- Protocolo: HTTP POST (JSON).
- Segurança: Assinatura HMAC-SHA256.
- Alterar arquitetura: SIM (Migração de Pull para Push).

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- Documentação da API de Eventos do iFood v1.0.
- Arquivo `app/services/ifood_service.py`.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- Novo router `app/routers/webhooks_ifood.py`.
- `app/services/ifood_service.py` atualizado.
- Script de validação `scripts/validation/verify_TASK-ESC-01.py`.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] Endpoint de Webhook retorna 200 OK para payloads válidos.
- [ ] Endpoint rejeita requisições com assinatura inválida (401/403).
- [ ] Pedido é criado no banco de dados imediatamente após o POST.
- [ ] O loop de polling original foi ajustado para 900 segundos.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/validation/verify_TASK-ESC-01.py`
RESULTADO_ESPERADO: Simulação de POST do iFood resulta em pedido no banco.

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Remover a rota de webhook.
- Reverter o intervalo de polling para 30 segundos no `ifood_service.py`.

🔒 11. PROIBIÇÕES EXPLÍCITAS
## PROIBIÇÕES
- É PROIBIDO processar o corpo do webhook sem validar a assinatura.
- É PROIBIDO realizar operações síncronas pesadas dentro da rota do webhook (usar BackgroundTasks).
