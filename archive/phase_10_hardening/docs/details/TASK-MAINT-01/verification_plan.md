# 🧪 Plano de Verificação: TASK-MAINT-01

## 1. Critérios de Sucesso (DoD)
- O diretório ignorar existe na raiz do projeto.
- A raiz do projeto contém apenas arquivos listados na SAFE_LIST.
- O script scripts/validation/verify_TASK-MAINT-01.py executa sem erros.
- A árvore de diretórios gerada pelo verificador está limpa e organizada.

## 2. Procedimento de Teste
1. Executar o comando: python scripts/maintenance/sanitize_repo.py.
2. Verificar visualmente se a pasta ignorar foi criada.
3. Executar o comando: python scripts/validation/verify_TASK-MAINT-01.py.
4. Confirmar que arquivos críticos como .env e a pasta app permanecem no lugar original.
