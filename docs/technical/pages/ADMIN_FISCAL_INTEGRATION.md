# 🧾 Módulo: Integração Fiscal (NFC-e)
**Domínio:** BACKEND / FISCAL
**Provedor:** Focus NFe v2

## 1. Fluxo de Emissão
O sistema utiliza um modelo assíncrono para não bloquear a finalização do pedido.

1.  **Gatilho:** Pedido marcado como `PAID`.
2.  **Orquestração:** `FiscalService` invoca o provedor configurado.
3.  **Comunicação:** O `FocusNFeProvider` envia o JSON via HTTPS com Basic Auth.
4.  **Retorno:** O sistema armazena a `nfe_key` e os links para PDF/XML no banco de dados.

## 2. Tratamento de Contingência
Caso a SEFAZ esteja offline ou o restaurante perca internet:
- O pedido é marcado com `fiscal_status = "error"`.
- O `Omni-Check` detecta falhas de emissão pendentes.
- O administrador pode disparar a re-emissão manual pela tela de Histórico.

## 3. Configurações (.env)
| Chave | Valor | Descrição |
| :--- | :--- | :--- |
| `FISCAL_PROVIDER` | `focus` | Ativa o driver da Focus NFe. |
| `FISCAL_ENV` | `sandbox` / `production` | Define o endpoint da API. |
| `FISCAL_PRODUCTION_CONFIRMED` | `true` | Trava de segurança para emissão real. |

## 4. Segurança
- **Idempotência:** O `order.id` é enviado como parâmetro `ref` para a Focus, impedindo a emissão duplicada da mesma nota em caso de retries.

