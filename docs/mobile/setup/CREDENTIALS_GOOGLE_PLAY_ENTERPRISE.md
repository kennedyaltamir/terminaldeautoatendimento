
# 🤖 Google Play Enterprise Credentials Report

**Objetivo:** Habilitar build e distribuição Android (Play Store).
**Custo:** US$ 25 (taxa única).
**Tempo Estimado:** Imediato (após pagamento).

## 1. Google Play Console
1. Acesse: [play.google.com/console](https://play.google.com/console).
2. Faça login com uma conta Google corporativa (recomendado).
3. Pague a taxa de registro de US$ 25.
4. Complete o perfil do desenvolvedor (Nome, Endereço).

## 2. Criar o Aplicativo
1. Clique em **"Create app"**.
2. **App name:** MesaFlow.
3. **Default language:** Portuguese (Brazil).
4. **App or Game:** App.
5. **Free or Paid:** Free (o app é gratuito, o serviço é pago fora).

## 3. Service Account (Para CI/CD)
O EAS precisa de uma "conta robô" para subir o `.aab` automaticamente.

1. Acesse: [Google Cloud Console](https://console.cloud.google.com).
2. Crie um novo projeto (ex: `mesaflow-mobile`).
3. No menu lateral, vá em **"IAM & Admin"** > **"Service Accounts"**.
4. Clique em **"Create Service Account"**.
   - Name: `eas-build-bot`.
   - Role: **Service Account User**.
5. Clique na conta criada > aba **"Keys"** > **"Add Key"** > **"Create new key"** > **JSON**.
6. O arquivo `.json` será baixado. **GUARDE-O COM A VIDA.**

## 4. Vincular Service Account na Play Store
1. Volte ao [Google Play Console](https://play.google.com/console).
2. Vá em **"Users and permissions"**.
3. Clique em **"Invite new users"**.
4. Cole o e-mail da Service Account (está dentro do JSON, campo `client_email`).
5. Em **App permissions**, adicione o app MesaFlow.
6. Em **Account permissions**, marque:
   - View app information.
   - Edit and delete draft apps.
   - Release to production, exclude devices, and use Play App Signing.
   - Manage testing tracks.
7. Clique em **"Invite user"**.

## 5. Configuração no GitHub Secrets
Abra o arquivo JSON baixado, copie TODO o conteúdo e adicione no GitHub:
- `GOOGLE_SERVICE_ACCOUNT_JSON`: (Cole o conteúdo do JSON aqui)

---
*MesaFlow Governance*

