# 🧪 Plano de Verificação: TASK-ENV-01

## 1. Critérios de Sucesso (DoD)
- [ ] Arquivo `.env.example` atualizado com todas as chaves do ecossistema v3.0+.
- [ ] Script `scripts/setup/audit_env.py` funcional.
- [ ] O script identifica chaves ausentes comparando o `.env` local com o `.env.example`.

## 2. Procedimento de Teste
1. Executar `python scripts/setup/audit_env.py`.
2. Verificar se o relatório aponta corretamente as variáveis que faltam no seu ambiente local.
3. Validar se o `.env.example` não contém segredos reais.
