
# 🔐 Guia de Credenciais: Apple & Google (Enterprise)

**Status:** BLOQUEANTE PARA BUILD
**Data:** Janeiro 2026

Para que o pipeline de CI/CD (`mobile_ci_cd.yml`) possa compilar e enviar o aplicativo para as lojas, as seguintes credenciais devem ser configuradas como **Secrets** no GitHub ou EAS.

---

## 🍎 Apple App Store (iOS)

### 1. Apple Developer Account
- **Onde:** [developer.apple.com](https://developer.apple.com)
- **Custo:** US$ 99/ano
- **Ação:** Criar conta do tipo "Organization" (recomendado para B2B).

### 2. App Store Connect
- **Onde:** [appstoreconnect.apple.com](https://appstoreconnect.apple.com)
- **Ação:** Criar um novo App.
- **Bundle ID:** Deve ser idêntico ao `ios.bundleIdentifier` no `app.json` (`com.mesaflow.app`).

### 3. Credenciais para CI/CD (Secrets)
No GitHub (Settings > Secrets > Actions), adicione:

| Secret Name | Descrição | Como Obter |
| :--- | :--- | :--- |
| `EXPO_APPLE_ID` | Seu Apple ID (email). | Login Apple. |
| `EXPO_APPLE_PASSWORD` | App-Specific Password. | [appleid.apple.com](https://appleid.apple.com) > Sign-in and Security > App-Specific Passwords. |
| `EXPO_APPLE_TEAM_ID` | Team ID (10 chars). | [developer.apple.com/account](https://developer.apple.com/account) (Membership Details). |

---

## 🤖 Google Play Store (Android)

### 1. Google Play Console
- **Onde:** [play.google.com/console](https://play.google.com/console)
- **Custo:** US$ 25 (taxa única)
- **Ação:** Criar conta de desenvolvedor.

### 2. Service Account (JSON)
O EAS precisa de permissão para enviar builds em seu nome.
1. Acesse o [Google Cloud Console](https://console.cloud.google.com).
2. Crie um projeto vinculado à sua conta Google Play.
3. Vá em **IAM & Admin > Service Accounts**.
4. Crie uma conta de serviço com a role **Service Account User**.
5. Crie uma chave JSON para esta conta e baixe o arquivo.
6. No Google Play Console, vá em **Users & Permissions** e convide o email da Service Account com permissão de **Release Manager**.

### 3. Credenciais para CI/CD (Secrets)
No GitHub, adicione:

| Secret Name | Descrição |
| :--- | :--- |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Conteúdo completo do arquivo JSON baixado (base64 opcional, mas texto plano funciona no GitHub). |

---

## 🔄 Próximos Passos
1. Configure os Secrets no GitHub.
2. Execute o comando de desbloqueio:
   ```bash
   # Apenas exemplo lógico
   git commit --allow-empty -m "chore: credentials configured"
   git push
   ```
3. O pipeline `build_deploy` será ativado automaticamente.

