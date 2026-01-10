# 📸 Especificação Técnica: TASK-MAINT-04
> **Título:** Automação de Captura de Telas Mobile (Mobile Visual Audit)
> **Status:** APROVADO
> **Objetivo:** Automatizar a captura de screenshots do emulador Android para documentação do App Nativo.

## 1. Metodologia de Captura
Como o aplicativo utiliza **Deep Linking** (configurado na TASK-039), o script utilizará comandos `adb` para forçar a navegação para rotas específicas e capturar o frame buffer do emulador.

## 2. Rotas Alvo
1. **Login:** `mesaflow://login`
2. **Garçom:** `mesaflow://waiter`
3. **Cozinha:** `mesaflow://kitchen`
4. **Entregador:** `mesaflow://driver`

## 3. Requisitos Técnicos
- **Ferramenta:** ADB (Android Debug Bridge) acessível via terminal.
- **Ambiente:** Emulador Android Studio ligado e com o app MesaFlow (Expo Go) carregado.
- **Output:** Imagens salvas em `docs/screenshots/mobile/`.
