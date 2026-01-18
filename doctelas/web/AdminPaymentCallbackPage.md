# 🔗 AdminPaymentCallbackPage
> **Plataforma:** WEB | **Domínio:** FINTECH | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Esta página atua como o "Handshake Final" entre o MesaFlow e os provedores de pagamento (Mercado Pago/Stripe). Sua função é capturar o código de autorização OAuth, trocá-lo por tokens de acesso e vincular a conta financeira do lojista ao seu Tenant no sistema.

## 2. Estrutura Técnica
- **OAuth Handler:** Lógica de captura de parâmetros de URL (`code`, `state`).
- **Security Validator:** Verifica se o parâmetro `state` corresponde ao ID da empresa logada para prevenir ataques de interceptação.
- **Status Stepper:** Visualização do progresso da conexão (Validando -> Vinculando -> Concluído).

## 3. Elementos Interativos
- **Botão de Retorno:** Link para voltar às configurações de pagamento em caso de erro.
- **Auto-Redirect:** Redirecionamento automático para o painel administrativo após o sucesso da operação.

## 4. Regras de Negócio (Integração)
- **Token Exchange:** O sistema realiza uma chamada server-side para converter o código temporário em um `access_token` permanente.
- **Credential Storage:** As credenciais são salvas de forma criptografada no banco de dados, habilitando o Pix Automático e Split de Pagamento.
- **Provider Mapping:** Atualiza o campo `payment_provider` da empresa para o provedor recém-conectado.

## 5. Estados e Cenários
- **Processing:** Spinner de alta prioridade enquanto a troca de tokens ocorre no backend.
- **Success:** Mensagem de celebração: "Conta conectada com sucesso!".
- **Failure:** Diagnóstico de erro (ex: "Código expirado" ou "Permissão negada pelo usuário").

## 6. Fluxo de Dados (API)
- **Inbound:** Recebe `GET /admin/payment/callback?code=...`
- **Outbound:** Dispara `POST /api/admin/payment/callback/{provider}` para finalização no backend.

---
*MesaFlow Fintech Infrastructure.*

