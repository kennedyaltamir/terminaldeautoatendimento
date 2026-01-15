
[[MESAFLOW_BEGIN:docs/tasks/TASK-FIX-01_KDS_404.md]]
# DOMAIN: BACKEND
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-FIX-01
TITLE: Correção de Resposta 404 em Rotas de Lista Vazia (KDS)
OWNER: Executor Kernel
PRIORITY: CRÍTICA (BLOCKER)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O endpoint `GET /api/admin/{slug}/service-requests` está registrado no FastAPI.
- Ao ser consultado quando não há chamados pendentes, ele retorna `404 Not Found`.
- Este comportamento quebra o `Promise.all` no Frontend do KDS, impedindo o carregamento dos pedidos.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- O endpoint `GET /api/admin/{slug}/service-requests` deve retornar `200 OK` e um JSON `[]` (lista vazia) quando não houver registros.
- O endpoint `GET /api/admin/{slug}/orders` deve ser verificado para garantir o mesmo comportamento resiliente.
- O KDS deve carregar com sucesso mesmo sem chamados ativos.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Refatoração de `app/routers/admin.py` (ou onde a rota estiver definida).
- Remoção de `raise HTTPException(404)` em casos de lista vazia.
- Verificação de outras rotas de listagem no mesmo arquivo.

### EXCLUI
- Alterações no Frontend (o erro é de contrato de API).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Manter compatibilidade com o Schema de resposta `List[ServiceRequestResponse]`.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `app/routers/admin.py`

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `app/routers/admin.py` corrigido.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] `debug_kds_failure.py` retorna 200 OK para a rota de service-requests.
- [ ] O retorno é uma lista vazia `[]` e não um objeto de erro.

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO