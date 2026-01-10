# 🆘 Guia de Solução de Problemas (Troubleshooting)

## 1. WebSockets não conectam
**Sintoma:** O KDS não atualiza sozinho. Erro no console: `WebSocket connection failed`.
**Causa:**
1.  O Backend não está rodando.
2.  Firewall bloqueando porta 8000.
3.  Uso de `https` no frontend mas `ws` (inseguro) no backend (Mixed Content).
**Solução:**
- Verifique se `python run.py` está ativo.
- Em produção (Render/Vercel), garanta que `NEXT_PUBLIC_WS_URL` comece com `wss://`.

## 2. Erro de Banco de Dados "Locked" ou "Connection Refused"
**Sintoma:** API retorna erro 500 em tudo.
**Causa:**
1.  PostgreSQL caiu.
2.  Muitas conexões abertas (Pool Exhausted).
**Solução:**
- Reinicie o Docker: `docker-compose restart db`.
- Verifique a URL no `.env`.

## 3. Frontend "Build Failed"
**Sintoma:** `npm run build` falha.
**Causa:**
1.  Erro de tipagem TypeScript.
2.  Variáveis de ambiente faltando no momento do build.
**Solução:**
- Rode `npm run lint` para ver os erros.
- No Render/Vercel, adicione as variáveis do `.env` no painel do projeto.

## 4. Imagens não carregam (Uploads)
**Sintoma:** Imagens quebradas no cardápio.
**Causa:**
1.  A pasta `frontend/public/uploads` não existe ou não tem permissão de escrita.
2.  Em produção (Serverless), o sistema de arquivos é efêmero (apaga ao reiniciar).
**Solução:**
- Local: Crie a pasta manualmente.
- Produção: Configure um Bucket S3 ou use serviços como Cloudinary (requer refatoração do `upload.py`).

## 5. Script `atualizar.py` falha no Windows
**Sintoma:** `PermissionError` ou `UnicodeDecodeError`.
**Solução:**
- Use a versão 3.2+ do script (já corrigida para encoding UTF-8 e paths do Windows).
- Evite ter pastas abertas no Explorer enquanto roda o script.
# 🆘 Guia de Solução de Problemas (Troubleshooting)

## 1. WebSockets não conectam
**Sintoma:** O KDS não atualiza sozinho. Erro no console: `WebSocket connection failed`.
**Causa:**
1.  O Backend não está rodando.
2.  Firewall bloqueando porta 8000.
3.  Uso de `https` no frontend mas `ws` (inseguro) no backend (Mixed Content).
**Solução:**
- Verifique se `python run.py` está ativo.
- Em produção (Render/Vercel), garanta que `NEXT_PUBLIC_WS_URL` comece com `wss://`.

## 2. Erro de Banco de Dados "Locked" ou "Connection Refused"
**Sintoma:** API retorna erro 500 em tudo.
**Causa:**
1.  PostgreSQL caiu.
2.  Muitas conexões abertas (Pool Exhausted).
**Solução:**
- Reinicie o Docker: `docker-compose restart db`.
- Verifique a URL no `.env`.

## 3. Frontend "Build Failed"
**Sintoma:** `npm run build` falha.
**Causa:**
1.  Erro de tipagem TypeScript.
2.  Variáveis de ambiente faltando no momento do build.
**Solução:**
- Rode `npm run lint` para ver os erros.
- No Render/Vercel, adicione as variáveis do `.env` no painel do projeto.

## 4. Testes Falhando com "AsyncMock"
**Sintoma:** `AssertionError: expected call not found` em testes que usam `await`.
**Causa:**
O `unittest.mock` às vezes cria novas instâncias de mocks ao acessar atributos.
**Solução:**
Atribua o mock explicitamente antes de passar para o patch:
```python
mock_post = AsyncMock()
mock_client.post = mock_post
# ... executa código ...
assert mock_post.called
```

## 5. Erro de UUID no SQLite
**Sintoma:** `AttributeError: 'str' object has no attribute 'hex'`.
**Causa:**
O SQLite não tem tipo UUID nativo e salva como string. O SQLAlchemy tenta tratar como objeto UUID.
**Solução:**
Use o tipo customizado `GUID` definido em `app/models.py` que trata essa compatibilidade automaticamente.
# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-08 10:30:00
# 🆘 Guia de Solução de Problemas (Troubleshooting)

## 1. Dados não aparecem (RLS)
**Sintoma:** A API retorna lista vazia `[]` ou 404 para recursos que você sabe que existem no banco.
**Causa:** O Row-Level Security (RLS) está bloqueando o acesso porque o contexto do tenant não foi definido corretamente.
**Solução:**
1.  Verifique se o Token JWT contém o `company_id` correto.
2.  Se estiver rodando scripts manuais ou testes, certifique-se de chamar `set_tenant(db, company_id)` antes da query.
3.  Verifique se o usuário do banco não é `superuser` (Superusers ignoram RLS, o que pode mascarar o problema em dev).

## 2. Erro "column company_id does not exist"
**Sintoma:** Erro 500 ao tentar rodar migrations ou acessar dados.
**Causa:** Uma migration de RLS tentou rodar em uma tabela que ainda não tinha a coluna `company_id`.
**Solução:**
- Rode `alembic upgrade head`. A migration `20260108_0005_add_company_id.py` foi criada especificamente para garantir essa coluna em todas as tabelas antes de aplicar o RLS.

## 3. Webhook iFood retornando 403
**Sintoma:** O iFood tenta enviar o pedido mas recebe erro.
**Causa:** Assinatura HMAC inválida.
**Solução:**
- Verifique se a variável de ambiente `IFOOD_WEBHOOK_SECRET` no servidor corresponde exatamente ao segredo configurado no Portal do Desenvolvedor do iFood.

## 4. Valores Monetários Incorretos (x100)
**Sintoma:** Um produto de R$ 10,00 aparece como R$ 1.000,00 ou R$ 0,10.
**Causa:** Confusão entre Decimal e Centavos.
**Solução:**
- O Backend (API) agora fala **Centavos** (Inteiros).
- O Frontend deve dividir por 100 apenas para exibir (`formatCurrency`).
- O Banco de Dados continua armazenando como `Numeric` (Decimal), a conversão é feita no Pydantic (Schema).

## 5. WebSockets não conectam
**Sintoma:** O KDS não atualiza sozinho. Erro no console: `WebSocket connection failed`.
**Solução:**
- Verifique se `python run.py` está ativo.
- Em produção (Render/Vercel), garanta que `NEXT_PUBLIC_WS_URL` comece com `wss://`.
