# 💰 Guia de Integração de Pagamentos

O MesaFlow possui um sistema híbrido de pagamentos que suporta dois modos de operação. Este documento explica como alternar entre eles.

## Modo 1: Pix Direto (Atual / Padrão)
Neste modo, o sistema gera um QR Code Pix estático (EMV QRCPS) usando a chave Pix cadastrada pelo restaurante.

*   **Fluxo:** Cliente Escaneia -> Dinheiro cai na conta do Restaurante -> Garçom confere -> Garçom dá baixa manual no KDS.
*   **Vantagens:** Sem taxas de intermediário, dinheiro imediato, não requer aprovação do Mercado Pago.
*   **Desvantagens:** Não tem baixa automática (tela do cliente não fica verde sozinha), não permite Split (comissão do SaaS).
*   **Como Ativar:**
    1.  Acesse o Painel Admin > Configurações.
    2.  Preencha o campo **Chave Pix**.
    3.  Certifique-se de que o campo `mp_access_token` no banco de dados está `NULL` ou vazio.

## Modo 2: Pix Automático (Mercado Pago)
Neste modo, o sistema usa a API do Mercado Pago para gerar um Pix dinâmico.

*   **Fluxo:** Cliente Escaneia -> Paga ao Mercado Pago -> MP avisa o sistema (Webhook) -> Pedido é aprovado automaticamente -> Dinheiro é dividido (Split).
*   **Vantagens:** Experiência mágica para o cliente (tela verde automática), Split de pagamento (SaaS recebe comissão automaticamente).
*   **Desvantagens:** Taxas do Mercado Pago (~0.99%), requer conta validada.
*   **Como Ativar:**
    1.  Obtenha o **Access Token de Produção** no painel do Mercado Pago Developers.
    2.  Rode o script de configuração ou insira no banco:
        ```bash
        python scripts/configurar_mp_real.py
        ```
    3.  Configure a URL pública (Webhook) no `.env` (em produção) ou via Ngrok (em dev).

## ⚠️ Solução de Problemas

### "O código QR não é válido"
*   **Causa:** O cálculo do CRC16 (assinatura do Pix) está incorreto ou a chave Pix contém caracteres inválidos.
*   **Solução:** O `PaymentService` já possui normalização de strings. Verifique se a chave Pix no admin não tem espaços extras.

### Webhook não chega (Tela não atualiza)
*   **Causa:** O Mercado Pago não consegue acessar `localhost`.
*   **Solução:** Use o **Ngrok** para criar um túnel público e atualize a variável `PUBLIC_API_URL` no `.env`.