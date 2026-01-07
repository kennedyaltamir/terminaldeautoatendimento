# 📱 Task 19: Identidade Operacional & Bootstrap de Sessão (Hardened)

## 1. Objetivo
Implementação da camada soberana de contexto operacional, eliminando dependências implícitas e valores fixos no aplicativo mobile.

## 2. Hardening Arquitetural (v1.1)
- **Centralização de Eventos:** Introduzido `mobile/src/types/realtime.events.ts` para evitar circularidade e inconsistência de tipos entre Store e Service.
- **Bootstrap Reativo:** O `AppStack` agora reage a mudanças no `authStatus`, garantindo que refreshes de token ou trocas de usuário re-sincronizem a `SessionStore` imediatamente.
- **Normalização de Handshake:** WebSocket service parametrizado para encerrar sessões antigas com códigos de status limpos antes de novas conexões.

## 3. Dívida Técnica Prioritária
- **Inestabilidade do Slug:** O slug derivado do e-mail é uma solução temporária. O Backend deve fornecer a claim `slug` no JWT na Missão 21.
- **Protocolo de Rede:** Migrar o token de Query String para Subprotocolo WebSocket.

---
*Fase 10 — Janeiro de 2026*
