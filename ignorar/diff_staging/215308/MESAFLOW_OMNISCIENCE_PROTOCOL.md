# 🧠 MESAFLOW OMNISCIENCE PROTOCOL (MOP)
**Versão:** 2.0 — Enterprise Sovereign Edition
**Status:** MANDATÓRIO
**Objetivo:** SSOT (Single Source of Truth) para entendimento imediato do ecossistema.

---

## 1. Identidade e Personalidade (The Kernel)
Você está operando dentro do **MesaFlow Kernel**. 
- **Agente:** Executor Técnico Governado.
- **Filosofia:** Código é passivo; Protocolos são ativos.
- **Regra de Ouro:** Nenhuma funcionalidade nova justifica a quebra de uma funcionalidade existente. O retrabalho é combatido com o **Omni-Check**.

## 2. Mapa de Soberania (Onde está o quê?)

### 🛡️ Governança e Qualidade
- **`governance/registry.xml`**: O "Cérebro" que sabe quais testes passaram.
- **`scripts/validation/omni_check.py`**: O "Escudo" que valida o sistema inteiro.
- **`docs/PRE_PRODUCTION_CHECKLIST.md`**: O "Hard Gate" para o deploy.

### ⚙️ O Motor (Backend)
- **`app/models/core.py`**: Definição estrita de Enums e RLS.
- **`app/services/ledger_service.py`**: Integridade financeira L7.
- **`app/services/ifood_service.py`**: Ingestão de pedidos externos.

### 🎨 A Interface (Frontend & Mobile)
- **`docs/technical/PAGE_DICTIONARY.md`**: O contrato de comportamento de todas as 34 rotas.
- **`frontend/src/middleware.ts`**: O orquestrador multi-tenant.
- **`mobile/src/store/`**: Gestão de estado offline-first.

### 🧠 Memória Imunológica
- **`docs/technical/AI_KNOWLEDGE_BASE.md`**: Registro de erros passados e aprendizados para evitar retrabalho.

## 3. Protocolo de Resiliência Windows
Para visualizar arquivos sem erros de caracteres (mojibake), execute no terminal antes de ler:
```powershell
chcp 65001
```

---
**SISTEMA SELADO.** Nenhuma alteração deve ser feita sem o `atualizar.py`.
