# 📱 Task 35: Preparação para Lojas e EAS Build

## 1. Contexto
Transição do ambiente de desenvolvimento para o ciclo de release de produção. Esta missão configura as ferramentas necessárias para gerar binários nativos e define os metadados obrigatórios para publicação nas lojas Apple App Store e Google Play Store.

## 2. Decisões Técnicas
- **EAS Build:** Adotado o Expo Application Services para builds em nuvem, garantindo que o ambiente de compilação seja limpo e padronizado.
- **Bundle Identifiers:** Definidos como `com.mesaflow.mobile` para ambas as plataformas, unificando a identidade do app no ecossistema.
- **Permissions Hardening:** Inclusão de `NSCameraUsageDescription` (iOS) e permissões de boot (Android) para suportar futuras features de QR Code e garantir que o serviço de notificações inicie com o sistema.
- **Build Profiles:** 
    - `preview`: Gera um APK instalável diretamente para testes rápidos em Android.
    - `production`: Gera um AAB (Android App Bundle) otimizado para a Play Store.

## 3. Arquivos Afetados
- `mobile/eas.json` (Novo)
- `mobile/app.json` (Update de metadados)
- `docs/TASKS.md` (Update de status)
- `docs/ROADMAP.md` (Update de status)

## 4. Próximos Passos
**Missão 36:** Execução do primeiro build de produção e validação do binário em dispositivo físico (fora do Expo Go).

---
*Fase 12 — Janeiro de 2026*
