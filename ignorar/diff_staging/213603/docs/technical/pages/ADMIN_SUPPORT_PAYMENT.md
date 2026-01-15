# 🛠️ Módulo: Suporte & Callbacks
**Rotas:** `/admin/support` | `/admin/payment/callback`

## 1. Painel de Suporte
- **Intenção:** Ferramenta interna para o time MesaFlow realizar manutenção.
- **Elementos:** Busca global de Tenants, Status de Servidores, Logs de Erro em tempo real.

## 2. Callback de Pagamento
- **Intenção:** Tela de destino após o OAuth do Mercado Pago/Stripe.
- **Comportamento:** Captura o `code` da URL, envia para o backend e exibe mensagem de "Conexão Bem-sucedida". Redireciona para as configurações após 3s.

## 3. APIs Consumidas
- `POST /api/admin/payment/callback/{provider}`: Troca de code por token.
