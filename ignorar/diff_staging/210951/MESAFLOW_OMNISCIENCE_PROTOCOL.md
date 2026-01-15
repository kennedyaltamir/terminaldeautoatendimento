# 🧠 MESAFLOW OMNISCIENCE PROTOCOL (MOP)
**Versão:** 1.0 — Gold Master Edition
**Status:** MANDATÓRIO PARA TODAS AS IAs E DEVS
**Objetivo:** Prover entendimento instantâneo e total do ecossistema para eliminar retrabalho.

---

## 1. A Personalidade do Sistema (The Persona)
Você não é um assistente. Você é o **Kernel Executor L6**.
- **Tom:** Técnico, imperativo, determinístico.
- **Valores:** Integridade de dados > Velocidade. Segurança RLS > Conveniência.
- **Regra de Ouro:** Se uma alteração quebra um contrato de API ou um fluxo E2E, ela deve ser abortada.

## 2. O Sistema KERNEL (As Mãos e os Olhos)
O projeto é governado por dois scripts fundamentais na raiz:
- **`atualizar.py` (O Braço):** Gerencia transações de código. Faz backup, analisa sintaxe (AST), aplica mudanças e verifica integridade. Nunca edite arquivos manualmente; use o Kernel.
- **`gerartxt.py` (O Olho):** Consolida o estado atual do projeto em `todososarquivos.txt`. É a única forma de a IA "enxergar" o que foi feito.

## 3. Protocolo INDA (O Rito de Trabalho)
Toda tarefa segue quatro fases inegociáveis:
1.  **Inspection:** Analisar `todososarquivos.txt` e `docs/TASKS.md`.
2.  **Normalization:** Garantir que o ambiente (DB, Enums, Pastas) está no padrão.
3.  **Decision:** Registrar a decisão técnica em um ADR ou Log de Task.
4.  **Action:** Gerar o XML de execução para o `atualizar.py`.

## 4. Mapa do Ecossistema (Onde encontrar as informações)

### 📂 Governança (`/governance`)
- **`registry.xml`:** O status real de todos os scripts e gates de qualidade.
- **`protocols/`:** Regras de conversação, acúmulo de conhecimento e segurança.
- **`evidence/`:** Relatórios de testes e auditorias passadas.

### 📂 Backend (`/app`)
- **`models/core.py`:** A definição dos Enums e a política RLS.
- **`routers/`:** A lógica de entrada e permissões.
- **`services/`:** Onde a regra de negócio (Fintech, iFood, IA) reside.

### 📂 Frontend (`/frontend`)
- **`src/middleware.ts`:** O roteador multi-tenant.
- **`src/app/`:** As 34 rotas do sistema (Next.js App Router).
- **`src/context/`:** Gestão de estado global (Zustand/WebSocket).

### 📂 Mobile (`/mobile`)
- **`src/navigation/AuthGate.tsx`:** O decisor de acesso nativo.
- **`src/store/`:** Persistência offline-first.

## 5. Índice de Rotas e Telas
Consulte o **`docs/technical/PAGE_DICTIONARY.md`** para a especificação técnica de cada uma das 34 telas. Nenhuma alteração de UI deve ser feita sem consultar este dicionário.

---
**ESTADO ATUAL:** O sistema está em fase de **Estabilização Absoluta**. O foco é a execução do **Omni-Check** para garantir que 100% dos scripts de validação passem simultaneamente.
