# 📝 Especificação Técnica: TASK-MOB-FIX-01
> **Título:** Diagnóstico e Correção de Boot do App Mobile
> **Status:** EM EXECUÇÃO
> **Objetivo:** Estabilizar o ambiente mobile (Expo) e garantir que o bundler inicie sem erros.

## 1. Diagnóstico de Infraestrutura
- **Correção do Generator:** O gerartxt.py estava ignorando a pasta mobile/. Corrigido para permitir que a IA veja o código.
- **Mobile Doctor:** Script para validar Node, Expo CLI, dependências e assets obrigatórios.
- **Emulator Debug:** Identificado problema de tela preta no emulador API 36.

## 2. Requisitos de Boot (Detectados)
- Node.js v18+ ou v20+.
- Expo SDK ~52.0.0 (Conforme detectado pelo Mobile Doctor).
- Assets obrigatórios: icon.png, splash.png, adaptive-icon.png, favicon.png.
- **Emulador:** Recomenda-se API 34 (Android 14) para maior estabilidade em desenvolvimento, evitando bugs da API 36 Preview.
