# DOMAIN: DOCUMENTATION
# TYPE: TASK
# STATUS: DONE
# 📋 TASK-DOC-02: Geração de Documentação de UI
## Objetivo
Transformar o inventário técnico JSON (gerado na TASK-QA-06) em documentação legível para humanos (Markdown), servindo como referência para designers, QAs e desenvolvedores.
## Implementação
- Criado script `scripts/documentation/generate_ui_docs.py`.
- O script consome `docs/audit/UI_INVENTORY_FULL.json`.
- Gera tabelas formatadas de elementos interativos.
- Identifica fluxos e estados automaticamente.
## Artefatos
- `scripts/documentation/generate_ui_docs.py`
- `docs/sds/UI_DOCS/FULL_UI_REFERENCE.md` (Gerado após execução)
## Como Executar
1. Garanta que o inventário JSON existe (`npm run inventory` em `scripts/automation`).
2. Execute o gerador de doc:
   ```bash
   python scripts/documentation/generate_ui_docs.py
   ```

