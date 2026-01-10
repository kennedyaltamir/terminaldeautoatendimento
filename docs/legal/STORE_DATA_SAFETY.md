# 📱 Guia de Preenchimento: Data Safety (Stores)

Este documento serve como referência técnica para o preenchimento dos formulários de privacidade da **Google Play Store** e **Apple App Store**.

---

## 🤖 Google Play Console (Data Safety Form)

### 1. Data Collection and Security
- **Does your app collect or share any of the required user data types?**
  - 👉 **Yes**
- **Is all of the user data collected by your app encrypted in transit?**
  - 👉 **Yes** (HTTPS/TLS 1.2+)
- **Do you provide a way for users to request that their data be deleted?**
  - 👉 **Yes** (Via privacy@mesaflow.com.br ou Link na Política de Privacidade)

### 2. Data Types
Selecione as seguintes categorias e configure como abaixo:

| Data Type | Collected? | Shared? | Purpose |
| :--- | :---: | :---: | :--- |
| **Name** | Yes | Yes (3rd Party) | App Functionality, Fraud Prevention |
| **Email Address** | Yes | Yes (3rd Party) | App Functionality, Account Management |
| **Phone Number** | Yes | Yes (3rd Party) | App Functionality (Notifications) |
| **User IDs** | Yes | No | App Functionality, Analytics |
| **Purchase History** | Yes | No | App Functionality |
| **Crash Logs** | Yes | No | Analytics (Sentry) |
| **Performance** | Yes | No | Analytics |
| **Device ID** | Yes | No | App Functionality, Fraud Prevention |

> **Nota sobre "Shared":** Marcamos "Yes" para Nome/Email/Telefone pois são enviados para processadores de pagamento (Mercado Pago/Stripe) e APIs de mensagem (WhatsApp), o que tecnicamente constitui compartilhamento para processamento externo.

---

## 🍎 Apple App Store Connect (App Privacy)

### 1. Data Types
- **Contact Info:** Name, Email Address, Phone Number.
- **Identifiers:** User ID, Device ID.
- **Usage Data:** Product Interaction.
- **Diagnostics:** Crash Data, Performance Data.
- **Purchases:** Purchase History.

### 2. Purpose & Tracking
Para cada tipo de dado, responda:

- **Data used to track you?**
  - 👉 **No**. (Não vendemos dados para ad networks).
- **Linked to the user?**
  - 👉 **Yes**. (Os dados são vinculados à conta do usuário para funcionamento do B2B).

### 3. Specific Purposes
- **App Functionality:** Name, Email, Phone, User ID, Purchases.
- **Analytics:** Crash Data, Performance Data, Product Interaction.
- **Fraud Prevention:** Device ID, Purchase History.

---
*Documento gerado para MesaFlow v3.1 (Enterprise)*