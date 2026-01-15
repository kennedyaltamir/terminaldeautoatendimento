# DOMAIN: BACKEND
# TASK_TYPE: KERNEL_INDA
# STATUS: IN_PROGRESS

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-AI-01
TITLE: Implementar Motor de Previsão de Demanda (Backend)
OWNER: Executor Kernel
PRIORITY: ALTA
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O sistema possui histórico de pedidos (`orders`, `order_items`), mas não utiliza esses dados para inteligência preditiva.
- O gestor não tem ferramentas para prever estoque ou escala de funcionários.
- Não existem bibliotecas de Data Science no ambiente.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Novo serviço `AiPredictionService` capaz de treinar um modelo simples (Regressão Linear) com base no histórico de vendas diárias.
- Endpoint `GET /api/admin/ai/forecast` que retorna a previsão de vendas para os próximos 7 dias.
- Inclusão de `scikit-learn` e `pandas` na stack.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Atualização de `requirements.txt`.
- Criação de `app/services/ai_prediction_service.py`.
- Criação de `app/routers/admin_ai.py`.
- Registro do router em `app/main.py`.
- Script de validação.

### EXCLUI
- Interface de UI (Frontend) nesta task.
- Modelos complexos (Prophet/LSTM) - MVP usa Regressão Linear.

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Libs: `scikit-learn`, `pandas`, `numpy`.
- Performance: O treinamento deve ser rápido ou cacheado (não treinar a cada request se o dataset for grande, mas para MVP pode ser on-the-fly com cache).

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- Dados da tabela `orders`.

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- JSON com datas e valores previstos.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] Endpoint retorna previsão para 7 dias.
- [ ] Modelo utiliza dados históricos reais do banco.
- [ ] Script de validação confirma acurácia básica (formato de saída).

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/validation/verify_TASK-AI-01.py`
