# 🧠 MesaFlow AI Knowledge Base (Immune System)
**Status:** APPEND-ONLY
**Objetivo:** Memória persistente para evitar repetição de erros técnicos.

---

### 2026-01-14 - Incidente Unicode Windows (Omni-Check)
- **Aprendizado:** Terminais Windows (cp1252) crasham ao imprimir emojis ou caracteres UTF-8 especiais via Python.
- **Prevenção:** Todo script de validação deve forçar `sys.stdout` para UTF-8 no boot se detectar plataforma `win32`.
- **Padrão de Correção:** Injetar o bloco de resiliência `io.TextIOWrapper` no topo de todos os scripts em `scripts/`.

### 2026-01-14 - Drift de Caminhos Físicos
- **Aprendizado:** O `omni_check.py` falhou ao procurar `inf_01_healthcheck.py` em `/governance` quando ele estava em `/comunication`.
- **Prevenção:** Seguir estritamente a RFC-SCRIPT-ORGANIZATION. Scripts de infra/saúde devem morar em `scripts/governance/`.
- **Ação:** Movido `inf_01_healthcheck.py` para o local canônico.
