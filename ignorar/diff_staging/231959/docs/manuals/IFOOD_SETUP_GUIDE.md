# 🍔 Guia de Configuração: Hub iFood

Este guia orienta a obtenção das credenciais necessárias para integrar sua loja do iFood ao MesaFlow OS.

## 1. Portal do Desenvolvedor
1. Acesse o [Portal do Desenvolvedor iFood](https://developer.ifood.com.br/).
2. Crie uma conta ou faça login.
3. Vá em **Minhas Aplicações** e crie uma nova aplicação do tipo "Merchant".

## 2. Credenciais Necessárias
Após a aprovação da aplicação, você terá acesso a:
- **Client ID:** Identificador único da sua aplicação.
- **Client Secret:** Chave secreta para gerar tokens.
- **Webhook Secret:** Chave usada para validar que as mensagens enviadas para o MesaFlow realmente vêm do iFood.

## 3. Configuração no .env
Insira as chaves no seu arquivo `C:\mesaflow\.env`:

```ini
IFOOD_CLIENT_ID=seu_client_id
IFOOD_CLIENT_SECRET=seu_client_secret
IFOOD_WEBHOOK_SECRET=seu_webhook_secret
```

## 4. Configuração do Webhook
No painel do iFood, configure a URL de destino para:
`https://seu-dominio.com/api/webhooks/ifood`

---
*MesaFlow OS — Conectando você aos grandes marketplaces.*
