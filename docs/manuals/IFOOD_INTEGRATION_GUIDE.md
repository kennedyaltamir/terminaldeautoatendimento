
# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-11 05:05:00
# 🍕 Guia de Integração iFood (MesaFlow Hub)

Este guia descreve como conectar sua loja do iFood ao MesaFlow para receber pedidos automaticamente no KDS.

---

## 1. Arquitetura da Integração
O MesaFlow utiliza uma abordagem híbrida **Push + Pull** para garantir que nenhum pedido seja perdido.

1.  **Webhook (Tempo Real):** O iFood envia uma notificação instantânea (`POST`) para o MesaFlow assim que um pedido é feito (`PLACED`).
2.  **Polling de Segurança (Fallback):** A cada 15 minutos, o MesaFlow consulta a API do iFood para buscar eventos que possam ter sido perdidos por falha na internet.

## 2. Configuração no Portal do Desenvolvedor iFood
Para ativar o recebimento em tempo real, você precisa configurar o Webhook no portal do iFood.

1.  Acesse o **Portal do Desenvolvedor iFood**.
2.  Vá em **Apps** > Selecione seu App > **Webhooks**.
3.  **URL de Callback:**
    *   Insira a URL da sua API de produção.
    *   Exemplo: `https://api.seurestaurante.com.br/api/webhooks/ifood/ifood`
4.  **Secret (Segredo):**
    *   Copie o segredo gerado pelo iFood.
    *   Adicione este valor na variável de ambiente `IFOOD_WEBHOOK_SECRET` no seu servidor (Render/Vercel).

## 3. Mapeamento de Cardápio
Para que os itens do iFood apareçam corretamente no KDS e deem baixa no estoque:

1.  No iFood, cada produto tem um **"Código PDV"** (ou SKU/External Code).
2.  No MesaFlow, vá em **Cardápio > Editar Produto**.
3.  Preencha o campo **"ID Externo"** com o mesmo código do iFood.

> **Nota:** Se o código não bater, o pedido entrará no sistema com um item genérico "Item não mapeado", exigindo atenção da cozinha.

## 4. Troubleshooting
Se os pedidos não estiverem chegando:

1.  Verifique se o servidor está online (`/api/health`).
2.  Verifique se o `IFOOD_WEBHOOK_SECRET` está correto (Logs mostrarão "Assinatura inválida").
3.  O Polling de segurança (15 min) garantirá que o pedido chegue eventualmente, mesmo se o Webhook falhar.

