
# 🚀 Checklist de Submissão: App Store & Play Store

Este documento define os critérios mínimos para que um binário MesaFlow seja submetido para revisão oficial.

## 1. Identidade e Assets
- [ ] **Ícones:** `icon.png` (1024x1024) sem transparência (iOS) e com safe-zone (Android).
- [ ] **Splash:** `splash.png` otimizado para diferentes densidades de tela.
- [ ] **Package Name:** Definido como `com.mesaflow.mobile` (Android) e `com.mesaflow.app` (iOS).

## 2. Segurança e Rede
- [ ] **Dynamic ENV:** Nenhuma referência a `localhost` ou IPs locais em `env.ts`.
- [ ] **SSL:** Todas as URLs de API e WebSocket utilizam `https://` e `wss://`.
- [ ] **Proguard:** Ofuscação de código ativa para Android (Release builds).

## 3. Conformidade Legal
- [ ] **Privacy Policy:** URL válida apontando para `/trust/security` no site oficial.
- [ ] **Data Safety:** Formulário de coleta de dados preenchido (Nome, Tel, Localização).
- [ ] **Permissions:** Apenas permissões estritamente necessárias (Vibrate, Internet, Camera).

## 4. Estabilidade Operacional
- [ ] **Error States:** Telas de 403, 500 e Offline validadas.
- [ ] **OTA Updates:** `expo-updates` configurado para o canal `production`.
- [ ] **Sentry:** DSN de produção configurado e capturando eventos.

---
*Aprovação Final: Architect Kernel v6.8*

