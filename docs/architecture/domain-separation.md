# 🏗️ Separação de Domínios e Governança de Contexto

## 1. Visão Geral
Para garantir a escalabilidade e a manutenibilidade do ecossistema MesaFlow, fica estabelecida a separação estrita entre os domínios de execução. Esta diretriz impede que alterações em uma plataforma (ex: Mobile) afetem inadvertidamente outra (ex: Web).

## 2. Regras de Ouro (G-Series)

### G1: Isolamento de Código
- O código do **MOBILE_APP** reside exclusivamente no diretório `mobile/`.
- O código do **WEB_APP** reside exclusivamente no diretório `frontend/`.
- O código do **BACKEND** reside exclusivamente no diretório `app/`.
- Scripts de automação e ferramentas de sistema residem em `scripts/` ou na raiz, sob o domínio **SHARED_INFRA**.

### G2: Consumo de Contratos
- As aplicações Mobile e Web são **estritamente consumidoras** dos contratos de API existentes.
- É proibido alterar o Backend ou os Schemas de dados para satisfazer necessidades de UI sem uma missão de arquitetura de Backend específica.

### G3: Declaração de Domínio
- Toda resposta emitida pela IA Executora deve declarar seu domínio de atuação na segunda linha, utilizando a tag `<Domain>`.
- Respostas que misturem alterações de múltiplos domínios (ex: Mobile + Backend) sem autorização explícita serão rejeitadas por violação de governança.

### G4: Infraestrutura Compartilhada (SHARED_INFRA)
- Alterações em scripts globais (`atualizar.py`, `gerartxt.py`, `verify_mobile_setup.py`) ou em documentação de governança devem ser classificadas como `SHARED_INFRA`.

## 3. Matriz de Responsabilidade

| Domínio | Diretório Alvo | Restrição Principal |
| :--- | :--- | :--- |
| **MOBILE_APP** | `mobile/` | Proibido tocar em `frontend/` ou `app/`. |
| **WEB_APP** | `frontend/` | Proibido tocar em `mobile/` ou `app/`. |
| **BACKEND** | `app/` | Proibido alterar lógica de UI. |
| **SHARED_INFRA** | `scripts/`, `docs/` | Foco em ferramentas e normas. |

---
*Versão 1.0 - Janeiro de 2026*
