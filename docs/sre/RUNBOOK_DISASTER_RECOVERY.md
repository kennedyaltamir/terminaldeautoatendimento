# DOMAIN: SRE
# LAST_MODIFIED: 2026-01-14 19:30:00

# 🆘 Runbook de Operações de Desastre (Day 2 Ops)

Este documento descreve os procedimentos técnicos para recuperação de falhas catastróficas e manutenção de segurança.

---

## 1. Recuperação de Banco de Dados (Database Restore)

**Cenário:** Perda total de dados, corrupção lógica ou deleção acidental em Produção (Neon.tech).

### Procedimento
1.  **Parar a Aplicação:**
    No dashboard do Render, suspenda o serviço `mesaflow-api` para evitar novas escritas.

2.  **Identificar o Point-in-Time (PITR):**
    Determine a hora exata do incidente (ex: 14:30 UTC). O restore deve ser feito para 14:29 UTC.

3.  **Executar Restore (Via Neon Console):**
    *   Acesse o Console do Neon.
    *   Selecione o Branch `main`.
    *   Clique em **Restore**.
    *   Selecione o timestamp desejado.
    *   Isso criará um *novo* branch (ex: `restore-1430`).

4.  **Promover Branch:**
    *   Renomeie o endpoint no `.env` do Render para apontar para o novo branch restaurado.
    *   OU promova o branch restaurado para `main` (se suportado pelo plano).

5.  **Validar Integridade:**
    Execute o script de integridade localmente apontando para o novo banco:
    ```bash
    python scripts/maintenance/system_integrity_check.py
    ```

6.  **Reiniciar Aplicação:**
    Retome o serviço no Render.

---

## 2. Rotação de Segredos (Secret Rotation)

**Cenário:** Vazamento de chaves de API (Stripe, Mercado Pago) ou saída de funcionário com acesso privilegiado.

### Procedimento: Stripe/MP

1.  **Gerar Novas Chaves:**
    *   Acesse o Dashboard do Stripe/MP.
    *   Revogue a chave antiga e gere uma nova (`sk_live_...`).

2.  **Atualizar Ambiente (Render):**
    *   Vá em **Environment** no Render.
    *   Atualize `STRIPE_SECRET_KEY`.
    *   O Render fará o redeploy automático.

3.  **Atualizar Ambiente (Local/Dev):**
    *   Informe a todos os devs para atualizarem seus `.env` locais.

4.  **Verificar Webhooks:**
    *   Se o `STRIPE_WEBHOOK_SECRET` mudou, atualize-o também.

---

## 3. Reset de Emergência do KDS (Redis Flush)

**Cenário:** O monitor de cozinha travou ou mostra pedidos fantasmas devido a estado corrompido no Redis.

### Procedimento

1.  **Acesso ao Redis:**
    Conecte-se via CLI ou ferramenta visual ao Redis de produção.

2.  **Limpar Chaves de Pedidos:**
    ```redis
    # CUIDADO: Isso limpa o cache de visualização, não o banco de dados.
    DEL mesaflow:orders:*
    ```

3.  **Forçar Re-sincronização:**
    O Frontend do KDS detectará a falha de conexão e forçará um `fetch` completo do PostgreSQL, restaurando a verdade.

---
*MesaFlow SRE Team*

