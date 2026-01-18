# DOMAIN: QA
# TYPE: TASK
# STATUS: DONE
# 📋 TASK-QA-06: Inventário Automatizado de UI
## Objetivo
Criar um mecanismo automatizado para mapear todas as telas, elementos interativos e fluxos da aplicação Web e Mobile, gerando uma documentação viva do estado atual da interface.
## Implementação
- Criado script `scripts/automation/generate_ui_inventory.js`.
- Implementada análise híbrida:
    - **Web:** Crawler dinâmico com Playwright (autenticado).
    - **Mobile:** Análise estática de código (Regex/AST simplificado).
- Saída estruturada em JSON compatível com ferramentas de documentação.
## Como Executar
1. Certifique-se de que o backend e frontend estão rodando (`python run.py`).
2. Instale as dependências do script:
   ```bash
   cd scripts/automation
   npm install
   ```
3. Execute o gerador:
   ```bash
   node generate_ui_inventory.js
   ```
4. Verifique o resultado em `docs/audit/UI_INVENTORY_FULL.json`.
## Artefatos Gerados
- `scripts/automation/generate_ui_inventory.js`
- `scripts/automation/package.json`

