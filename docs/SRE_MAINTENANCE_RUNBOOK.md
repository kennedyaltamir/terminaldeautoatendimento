# 🛠️ SRE Maintenance & Disaster Recovery Runbook

## 1. Falha no Redis (Cache/WebSockets)
**Sintoma:** KDS não atualiza em tempo real ou erro "Timeout connecting to server".
**Ação:**
1.  Verifique o status no painel do Upstash/Render.
2.  O MesaFlow possui fallback automático para memória local. Se o Redis cair, reinicie a API para que ela entre em modo `bypass`.
3.  **Nota:** No modo bypass, o broadcast só funciona entre clientes conectados ao mesmo worker.

## 2. Debug de Integração iFood
**Sintoma:** Pedidos do iFood não aparecem no KDS.
**Ação:**
1.  Verifique os logs do backend procurando por `[iFood]`.
2.  Valide se o `ifood_token` da empresa não expirou.
3.  Use o script `scripts/tests/test_ifood_integration.py` para simular um payload e ver onde a conversão falha.

## 3. Limpeza de Cache Next.js
**Sintoma:** Alterações no cardápio não refletem para o cliente final.
**Ação:**
Execute o script de manutenção:
```bash
python scripts/maintenance/clean_next_cache.py
```

## 4. Reset de Banco de Dados (Emergência)
Para recriar o ambiente do zero preservando a estrutura:
```bash
python scripts/maintenance/seed.py
```
*⚠️ CUIDADO: Este comando apaga todos os dados de produção se executado com a DATABASE_URL de prod.*

---
# 🛠️ SRE & Ops Runbook: Manutenção de Produção

## 1. Diagnóstico de Banco de Dados (Neon)
Se a API estiver lenta, verifique o número de conexões ativas.
**Comando para ver conexões (SQL):**
```sql
SELECT count(*) FROM pg_stat_activity WHERE datname = 'neondb';
```
Se estiver próximo ao limite, reinicie o serviço no Render para forçar o fechamento de conexões zumbis.

## 2. Recuperação de Redis
Se o KDS parar de atualizar:
1.  Acesse o terminal do Backend.
2.  Verifique se o Redis responde: `redis-cli -u $REDIS_URL ping`.
3.  Se falhar, altere a variável `REDIS_URL` para vazio no Render. O sistema entrará em modo **Local Memory**, restaurando a operação básica.

## 3. Logs de Erro iFood
Para ver falhas de integração em tempo real:
```bash
# No terminal do Render/Docker
grep "\[iFood\]" app.log
```
**Erros comuns:**
- `401 Unauthorized`: O token da empresa no iFood expirou. O dono deve refazer o login via OAuth.
- `403 Forbidden`: O `merchant_id` está incorreto.

## 4. Limpeza de Cache de Build
Se o frontend apresentar bugs visuais após um deploy:
1.  Vá ao painel da Vercel.
2.  Clique em **Redeploy**.
3.  Marque a opção **"Clean Build Cache"**.

---

