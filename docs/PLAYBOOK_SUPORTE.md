# 🆘 Playbook de Suporte Técnico (Nível 2)

Guia de diagnóstico para administradores do sistema e suporte técnico.

---

## 1. Troubleshooting de WebSocket
**Sintoma:** "O pedido não aparece na cozinha" ou "A tela não atualiza sozinha".

**Diagnóstico:**
1.  Verifique se o cliente está online (ícone de Wi-Fi verde no sistema).
2.  Abra o Console do Navegador (F12). Procure por erros em vermelho: `WebSocket connection failed`.
3.  **Causa Comum:** Firewall da rede corporativa bloqueando a porta ou protocolo `wss://`.
4.  **Solução:** Testar no 4G. Se funcionar no 4G, o problema é a rede local do restaurante.

---

## 2. Falhas de Pagamento
**Sintoma:** "O cliente pagou o Pix mas a tela não ficou verde".

**Diagnóstico:**
1.  Acesse o Dashboard do **Mercado Pago** (ou Stripe).
2.  Busque a transação pelo valor ou data.
3.  **Cenário A (Não consta):** O cliente não pagou ou pagou para o QR Code errado.
4.  **Cenário B (Consta como Pago):** O Webhook falhou.
    *   Verifique os logs do servidor: `heroku logs --tail` ou painel do Render.
    *   Procure por `POST /api/webhooks/mercadopago`. Se não houver registro, o MP não conseguiu chamar sua API (Erro de DNS ou Servidor fora do ar).
5.  **Solução Paliativa:** No Painel Admin, vá no pedido e clique em "Confirmar Pagamento" manualmente para liberar a cozinha.

---

## 3. Reset de Emergência
**Sintoma:** "O sistema está travado/lento em uma máquina específica".

**Procedimento:**
1.  O MesaFlow usa muito cache local (`localStorage`) para velocidade.
2.  Peça para o usuário pressionar `Ctrl + Shift + R` (Hard Refresh).
3.  Se não resolver, limpar dados do site: F12 > Application > Storage > Clear Site Data.
4.  **Atenção:** Isso desloga o usuário. Tenha a senha em mãos.

---

## 4. Scripts SQL Úteis
Para correções diretas no banco de dados quando a API não for suficiente.

**Liberar uma mesa travada (Status 'occupied' sem sessão ativa):**
```sql
UPDATE tables 
SET is_active = true 
WHERE table_number = X AND company_id = 'UUID_DA_EMPRESA';

-- Verificar se há sessão órfã
SELECT * FROM table_sessions WHERE table_id = X AND is_active = true;
-- Matar sessão órfã
UPDATE table_sessions SET is_active = false, closed_at = NOW() WHERE id = Y;

Resetar senha de Admin manualmente:
-- A senha hash deve ser gerada via script Python (bcrypt)
UPDATE companies 
SET password_hash = '$2b$12$...' 
WHERE owner_email = 'admin@cliente.com';