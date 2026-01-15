
# 🔐 Relatório de Credenciais de Produção (Mobile)

## 1. Google Play Store (Android)
- **Portal:** [Google Play Console](https://play.google.com/console)
- **Ação:** Criar conta de desenvolvedor ($25 USD, taxa única).
- **Credencial Necessária:** `service-account.json` (Google Cloud IAM).
- **Permissões:** "Release Manager" para upload de AAB.

## 2. Apple App Store (iOS)
- **Portal:** [Apple Developer Program](https://developer.apple.com)
- **Ação:** Enrolment ($99 USD/ano).
- **Credencial Necessária:** `Auth Key` (.p8 file) para App Store Connect API.
- **Certificados:** Distribution Certificate + Provisioning Profile (Gerenciados pelo EAS).

## 3. Sentry (Telemetria)
- **Portal:** [Sentry.io](https://sentry.io)
- **Ação:** Criar projeto "MesaFlow Mobile".
- **Credencial:** `DSN` (Data Source Name).
- **Configuração:** Adicionar em `mobile/.env` como `EXPO_PUBLIC_SENTRY_DSN`.

## 4. Expo (EAS Build)
- **Portal:** [Expo.dev](https://expo.dev)
- **Ação:** Criar organização e projeto.
- **Credencial:** `EXPO_TOKEN` (Access Token nas configurações de conta).
- **Uso:** CI/CD GitHub Actions.

---
*Gerado automaticamente pelo Kernel L6.*

