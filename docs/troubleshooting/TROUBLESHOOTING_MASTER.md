# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-08 23:55:00
# 🔧 TROUBLESHOOTING MASTER LOG (TML)

> **Versão:** 1.3
> **Classificação:** KNOWLEDGE_BASE
> **Status:** ATIVO
> **Mantenedor:** Executor Kernel

## 1. Objetivo
Este documento atua como a **Memória Imunológica** do projeto. Ele registra erros passados, suas causas raízes e a solução definitiva, impedindo a recorrência de falhas conhecidas e acelerando o diagnóstico de incidentes.

## 2. Matriz de Erros e Soluções (Rigid Table)

| ID | Código de Erro | Contexto / Sintoma | Causa Raiz (Root Cause) | Solução Definitiva (Fix) | Regra de Prevenção (Policy) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TS-001** | `FFP-01` | `RUÍDO DETECTADO: Zero texto permitido fora do envelope XML.` | A IA gerou texto conversacional antes ou depois das tags XML. | Limpeza manual do `resposta.txt` e reeducação do prompt. | **AI_OPTIMIZATION_LAYER:** `Narrative_Text: DISABLED`. |
| **TS-002** | `FFP-02` | `Omissão detectada: '...'` ou `restante do código`. | A IA tentou economizar tokens enviando arquivos parciais. | Uso do `atualizar.py` v2.4 com **Interactive Override** ou reescrita integral. | **System_Persona:** `Rule R1: Entrega Integral Obrigatória`. |
| **TS-003** | `FFP-06` | `Tentativa de alteração não autorizada em arquivo protegido`. | A IA tentou modificar `docs/governance` sem a tag de override. | Adição da tag `<Governance_Override>` no XML de resposta. | **UEP v2.1:** `Governance_Override` é mandatório para Kernel. |
| **TS-004** | `NDK_MISMATCH` | Erro de build Android: `No version of NDK matched`. | O projeto Expo SDK 54 exige NDK 26.1, mas o ambiente tinha 27.x. | Script `force_ndk_26.py` para injetar versão exata no `build.gradle`. | **Mobile Setup:** Validar `ndkVersion` antes do build. |
| **TS-005** | `WEB_BUNDLE_ERR` | Tela branca no navegador: `SyntaxError: import.meta`. | O Metro Bundler não transpilava corretamente módulos ESM para Web. | Configuração de `metro.config.js` com `unstable_allowModuleTransforms`. | **Web Config:** Forçar transpilação de `node_modules`. |
| **TS-006** | `LINT_FAIL` | `Suspense Boundary` faltando no Next.js. | Componentes que usam `useSearchParams` não estavam em Suspense. | Wrap do componente em `<Suspense>` no `page.tsx`. | **Next.js Rules:** Client Components com SearchParams exigem Suspense. |
| **TS-007** | `DB_LOCK` | Erro de conexão `too many clients` no Postgres. | Conexões não fechadas ou falta de Pooler em ambiente Serverless. | Uso de `pgbouncer` (Neon) e `pool_pre_ping=True` no SQLAlchemy. | **Infra:** Sempre usar Connection Pooling em Prod. |
| **TS-008** | `NPM_MISSING_SCRIPT` | `npm error Missing script: "test"` | O `package.json` não possui a entrada `"test": "jest"`. | Executar `scripts/maintenance/fix_mobile_test_script.py`. | **Mobile Setup:** Validar `package.json` antes de rodar validações. |
| **TS-009** | `JEST_ESM_ERR` | `Unexpected token 'export'` em testes. | Jest não transpilava módulos ESM em `node_modules`. | Configurar `transformIgnorePatterns` no `jest.config.js`. | **Mobile Test:** Jest deve transformar explicitamente libs Expo. |
| **TS-010** | `RNTL_MISMATCH` | `Unexpected token 'export'` no `detectHostComponentNames`. | Incompatibilidade entre RNTL < 13 e React Native 0.76+. | Upgrade para `@testing-library/react-native@^13.0.0`. | **Mobile Deps:** RN 0.76 exige RNTL v13+. |
| **TS-011** | `POLLING_SATURATION` | Latência alta em pedidos de mesa quando o iFood está ativo. | O loop de polling de 30s consome todo o I/O de rede. | Migrar para Inbound Webhooks (TASK-ESC-01). | **Architecture:** Proibido polling infinito para serviços externos. |
| **TS-012** | `TENANT_LEAK_RISK` | Risco de acesso a dados de outra empresa por erro de código. | Isolamento depende de filtragem manual no código Python. | Implementar PostgreSQL RLS (TASK-SEC-01). | **Security:** Isolamento deve ser via Hardware/DB Engine. |
| **TS-013** | `FLOAT_DRIFT` | Diferença de centavos em relatórios financeiros. | Uso de `number` (float64) no JavaScript para cálculos monetários. | Refatorar para Centavos/Inteiros (TASK-FIN-01). | **Fintech:** Proibido trafegar floats em valores monetários. |
| **TS-014** | `BATT_DRAIN_MOB` | Aquecimento e drenagem de bateria no App do Garçom. | Global Clock de 5s processando SLA ininterruptamente. | Otimizar ciclo de vida do Clock (TASK-MOB-01). | **Mobile:** Timers devem respeitar o AppState. |
| **TS-015** | `MISSING_BOTO3` | `ModuleNotFoundError: No module named 'boto3'`. | Dependência de storage adicionada mas não instalada no ambiente. | Adicionar `boto3` ao `requirements.txt` e rodar `pip install`. | **Ops:** Validar deps antes de rodar scripts de infra. |
| **TS-016** | `INVALID_API_KEY` | `stripe.error.AuthenticationError`. | Chave de API inválida ou expirada no `.env`. | Verificar credenciais no dashboard do provedor e atualizar `.env`. | **Ops:** Pre-flight check deve validar auth, não apenas formato. |
| **TS-017** | `SCA_VULN` | Vulnerabilidades críticas reportadas pelo `pip-audit`. | Dependências desatualizadas com CVEs conhecidos. | Atualizar pacotes para versões corrigidas (`requirements.txt`). | **Security:** SCA deve rodar em todo build de produção. |

---

## 3. Procedimento de Registro
Sempre que um novo erro **bloqueante** for resolvido, ele deve ser catalogado aqui seguindo estritamente o formato da tabela acima. O registro deve ser feito na mesma task que aplicou a correção.

1.  **Identifique** o padrão do erro.
2.  **Isole** a causa raiz (não o sintoma).
3.  **Codifique** a solução em um script ou regra.
4.  **Registre** nesta tabela.
