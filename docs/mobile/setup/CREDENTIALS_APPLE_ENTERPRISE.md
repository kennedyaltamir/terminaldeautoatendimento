
# 🍎 Apple Enterprise Credentials Report

**Objetivo:** Habilitar build e distribuição iOS (App Store).
**Custo:** US$ 99/ano.
**Tempo Estimado:** 2-5 dias úteis (validação D-U-N-S).

## 1. Apple Developer Account (Organization)
Para empresas, você **NÃO** deve usar conta pessoal.
1. Acesse: [developer.apple.com/enroll](https://developer.apple.com/enroll).
2. Selecione **"Organization"** (não Individual).
3. **Requisito Crítico:** D-U-N-S Number.
   - Se não tiver, solicite gratuitamente na Apple (demora 2 dias).
   - O nome da empresa no D-U-N-S deve ser IDÊNTICO ao cadastro legal.
4. Pague a taxa de US$ 99.

## 2. App Store Connect
Após aprovação da conta:
1. Acesse: [appstoreconnect.apple.com](https://appstoreconnect.apple.com).
2. Vá em **"My Apps"** > **"+"** > **"New App"**.
3. Preencha:
   - **Name:** MesaFlow (deve ser único na loja).
   - **Primary Language:** Portuguese (Brazil).
   - **Bundle ID:** Selecione `com.mesaflow.app` (se não aparecer, crie em Certificates).
   - **SKU:** `mesaflow-mobile-v1`.

## 3. Credenciais para CI/CD (GitHub/EAS)
O EAS Build gerencia os certificados, mas precisa de acesso.

### A. Apple ID (Username)
- O e-mail da conta com permissão de "Admin" ou "App Manager".

### B. App-Specific Password (Senha)
Necessário para bypassar 2FA no CI.
1. Acesse: [appleid.apple.com](https://appleid.apple.com).
2. Login > **Sign-in and Security** > **App-Specific Passwords**.
3. Clique em "+", nomeie como "EAS Build" e copie a senha (ex: `abcd-efgh-ijkl-mnop`).

### C. Team ID
1. Acesse: [developer.apple.com/account](https://developer.apple.com/account).
2. Role até **"Membership Details"**.
3. Copie o **Team ID** (10 caracteres, ex: `X1Y2Z3A4B5`).

## 4. Configuração no GitHub Secrets
Adicione estas chaves no seu repositório:
- `EXPO_APPLE_ID`: (Seu email)
- `EXPO_APPLE_PASSWORD`: (Senha gerada no passo 3B)
- `EXPO_APPLE_TEAM_ID`: (Team ID do passo 3C)

---
*MesaFlow Governance*

