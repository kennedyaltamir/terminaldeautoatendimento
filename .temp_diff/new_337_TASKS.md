# 📋 Backlog Mestre de Tarefas: MesaFlow

## ✅ Concluído Recentemente (Fase 11 & 12 - Mobile)
- [x] **Build Nativo:** APK v1.0.1 gerado com correções semânticas.
- [x] **Auth Hardening:** Missão 14A (Validação de Claims e Decodificação Resiliente).
- [x] **Infra:** Auditoria Mestre de alinhamento (`master_alignment_check.py`).
- [x] **POS:** Fluxo completo de Venda, Pagamento e Impressão (Lógica).

---

## 🚀 Próximas Prioridades (Fila de Execução)

### 1. [Mobile] Missão 36: Build Local (Android Studio) 🏗️
**Complexidade:** Média | **Impacto:** Produtividade
*   **O que fazer:** Executar `npx expo prebuild` e validar a geração do APK via Gradle localmente, garantindo independência da nuvem EAS.
*   **Status:** Guia `LOCAL_BUILD_GUIDE.md` criado. Aguardando execução.

### 2. [Mobile] Missão 37: Homologação de Impressão em Campo 🖨️
**Complexidade:** Alta | **Impacto:** Operacional
*   **O que fazer:** Testar a comunicação Bluetooth com uma impressora térmica real (Zebra/Goojprt) utilizando o APK gerado.

### 3. [Mobile] Missão 38: Sentry Native Integration 📊
**Complexidade:** Média | **Impacto:** Observabilidade
*   **O que fazer:** Integrar SDK do Sentry para React Native.

### 4. [Backend] Otimização de Queries KDS ⚡
**Complexidade:** Média | **Impacto:** Performance
*   **O que fazer:** Criar índices compostos para queries de `orders` filtradas por `status` e `created_at`.
