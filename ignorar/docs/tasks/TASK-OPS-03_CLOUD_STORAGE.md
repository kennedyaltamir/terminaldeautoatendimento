# DOMAIN: OPERATIONS
# TASK_TYPE: KERNEL_INDA
# STATUS: DONE

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-OPS-03
TITLE: Cloud Object Storage (S3/R2 Integration)
OWNER: Executor Kernel
PRIORITY: CRÍTICA (DATA PERSISTENCE)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O sistema salva uploads de imagens (Logos, Produtos) no sistema de arquivos local (`frontend/public/uploads`).
- Em ambientes de produção PaaS (Render, Heroku, Vercel), o sistema de arquivos é **efêmero**.
- **Consequência Crítica:** Todas as imagens enviadas pelos usuários são deletadas automaticamente a cada deploy ou reinício do servidor.
- Isso inviabiliza a operação real do cardápio digital.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Implementação de um `StorageService` agnóstico que suporta protocolo S3 (AWS S3, Cloudflare R2, MinIO).
- Uploads são enviados para um Bucket na nuvem e a URL pública é retornada.
- Fallback transparente: Se as credenciais de nuvem não estiverem presentes (Dev), continua usando disco local.
- Persistência garantida de assets em produção.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Adição da biblioteca `boto3` em `requirements.txt`.
- Criação de `app/services/storage_service.py`.
- Refatoração de `app/routers/upload.py` para usar o serviço.
- Atualização de `.env.production.template` com credenciais AWS/S3.
- Atualização de `scripts/production/validate_integrations.py` para testar acesso ao Bucket.
- Atualização do `docs/TASKS.md`.

### EXCLUI
- Migração de arquivos já existentes no disco local para a nuvem.
- CDN (Cloudfront) - usaremos a URL direta do S3/R2 por enquanto.

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Lib: `boto3` (Padrão de mercado).
- Segurança: Arquivos devem ser públicos (ACL public-read) ou usar Presigned URLs (optamos por Public Read para cardápio).
- Naming: UUIDv4 para evitar colisão de nomes.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- `app/routers/upload.py`

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `requirements.txt`
- `app/services/storage_service.py`
- `app/routers/upload.py`
- `.env.production.template`
- `scripts/production/validate_integrations.py`

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [x] `requirements.txt` contém `boto3`.
- [x] `StorageService` detecta configuração de S3 e usa se disponível.
- [x] `upload.py` delega a lógica de salvamento para o serviço.
- [x] Script de validação conecta no Bucket e lista objetos (ou verifica permissão).

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `python scripts/production/validate_integrations.py`
RESULTADO_ESPERADO: "STORAGE: OK" (se configurado) ou "STORAGE: WARN" (se local).

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter `app/routers/upload.py`.
- Remover `app/services/storage_service.py`.
- Remover `boto3` de `requirements.txt`.
