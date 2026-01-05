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
