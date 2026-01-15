
# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-13 09:45:00

# 🔄 PROMPT DE TRANSFERÊNCIA: OPERAÇÃO OMNISCIENCE (AUDITORIA TOTAL)

**Sistema:** MesaFlow OS
**Estado Atual:** 🟢 STABLE (API Fixed & Docker Optimized)
**Protocolo:** INDA Strict (Inspection · Normalization · Decision · Action)
**Objetivo:** Validação Funcional Completa e Catalogação Absoluta.

---

## 1. CONTEXTO IMEDIATO
Acabamos de corrigir falhas críticas de serialização (Pydantic v2) e rotas inexistentes (`admin_history`).
O Backend está respondendo corretamente (`200 OK` e `401 Unauthorized` onde esperado).
O Docker está otimizado (`.dockerignore` configurado).

**A missão agora muda de "Correção" para "Certificação Total".**

---

## 2. OBJETIVOS DA SESSÃO (MANDATÓRIOS)

Você deve executar uma varredura completa no sistema para garantir que **nada** foi deixado para trás.

### 🗺️ A. Mapeamento de Rotas (Backend & Frontend)
1.  **Backend:** Listar todos os endpoints do FastAPI (`app/routers`).
2.  **Frontend:** Listar todas as páginas do Next.js (`src/app`).
3.  **Validação:** Testar o status HTTP de cada rota (esperado: 200, 401 ou 403. Nunca 404 ou 500).

### 🖱️ B. Catalogação de Elementos de Interação
1.  Executar o `enterprise_ui_explorer_v5_1.py` em modo **INVENTORY**.
2.  Gerar um mapa de todos os botões, inputs e links do sistema.
3.  Verificar se algum elemento leva a "Dead Ends" (ações sem resposta).

### 📜 C. Catalogação de Scripts (Registry Alignment)
1.  Ler recursivamente a pasta `scripts/`.
2.  Cruzar com `comunication/registry.xml`.
3.  **Ação:** Se um script existe no disco mas não no XML, adicione-o ou delete-o (se for lixo). Se está no XML mas não no disco, remova do XML.

### 🧪 D. Teste Funcional Sistêmico
1.  Executar fluxo E2E completo:
    *   Criar Pedido (Cliente) -> Receber no KDS (Cozinha) -> Finalizar (Garçom) -> Auditar (Admin).
2.  Validar se os dados fluem corretamente entre os módulos sem erros de tipo.

---

## 3. ARTEFATOS DE SAÍDA ESPERADOS

Ao final desta sessão, você deve entregar:

1.  **`docs/audit/FULL_ROUTE_MAP.md`**: Lista de todas as rotas e seus status reais.
2.  **`docs/audit/UI_INTERACTION_CATALOG.md`**: Inventário de botões e inputs por tela.
3.  **`comunication/registry.xml`**: Versão Final (Gold Master), 100% sincronizada.
4.  **`comunication/reports/REPORT_OMNISCIENCE.md`**: Relatório final de integridade.

---

## 4. RESTRIÇÕES (NON-NEGOTIABLES)

*   **NÃO** assuma que uma rota funciona só porque o código existe. Teste com `curl` ou script Python.
*   **NÃO** ignore erros de console no Frontend.
*   **NÃO** deixe scripts "órfãos" na pasta `scripts/`. Tudo deve estar catalogado.

---

## 5. COMANDO INICIAL

Inicie executando o mapeamento de rotas para estabelecer o território:

```bash
python scripts/automation/map_routes.py
```

Em seguida, valide a integridade do registro atual antes de expandi-lo:

```bash
python comunication/scripts/gov_04_registry_drift.py
```

**MesaFlow Kernel L6 — Execute a Auditoria Total.**

