# ♾️ Manual de DevOps e CI/CD

Este documento descreve como o código sai da sua máquina e chega aos servidores de produção (Render/Vercel) com segurança.

## 1. O Pipeline de Automação (GitHub Actions)
Toda vez que você faz um `git push`, o arquivo `.github/workflows/ci.yml` é acionado.

### O que ele faz?
1.  **Backend Job:**
    *   Sobe um banco PostgreSQL temporário (Docker).
    *   Instala Python e dependências.
    *   Roda as migrações do Alembic.
    *   Executa todos os testes (`pytest`).
2.  **Frontend Job:**
    *   Instala Node.js.
    *   Roda `npm run build` para verificar se não há erros de TypeScript ou sintaxe que quebrariam a Vercel.

### Status do Deploy
*   ✅ **Verde:** O código passou nos testes. O Render/Vercel prosseguirão com o deploy automático.
*   ❌ **Vermelho:** Algo quebrou. O deploy deve ser interrompido ou revertido. Verifique a aba "Actions" no GitHub.

## 2. Validação Local (Antes do Push)
Para evitar "sujar" o histórico do Git com tentativas falhas, rode o validador local:

```bash
python scripts/setup/ci_validate.py
```

## 3. Estratégia de Branches
*   `main`: **Produção**. Código estável e testado. Deploy automático.
*   `develop` (ou feature-branches): Desenvolvimento. Pull Requests para a `main` disparam o CI para validação.

## 4. Monitoramento
*   **Render:** Dashboard > Logs (para erros de runtime do Python).
*   **Vercel:** Dashboard > Deployments (para erros de build do Next.js).
*   **Sentry:** Captura de exceções em tempo real (se configurado).
