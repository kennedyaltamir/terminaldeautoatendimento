
# 📝 Execution Checklist: TASK-GOV-10
> **RFC-010: Enum Lifecycle & Deprecation Policy**

## 1. Fase de Pesquisa
- [ ] Mapear Enums críticos em `app/models/core.py`.
- [ ] Identificar dependências de Enums no Mobile (Zustand) e Frontend.

## 2. Fase de Redação
- [ ] Definir estados do ciclo de vida (`ACTIVE`, `DEPRECATED`, `RETIRED`).
- [ ] Criar matriz de compatibilidade (Versão API vs Versão App).
- [ ] Estabelecer política de "Grace Period" para remoção de valores.

## 3. Fase de Validação
- [ ] Revisão por Architect Kernel.
- [ ] Simulação teórica de mudança de status (ex: `OrderStatus`).
- [ ] Aprovação e congelamento da RFC.

---
*Este checklist deve ser preenchido durante a execução da task.*

