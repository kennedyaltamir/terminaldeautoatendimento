# ⏪ Plano de Rollback: TASK-MOB-FIX-01

## 1. Procedimento
- Reverter alterações no `mobile/package.json` e `mobile/app.json` via Git.
- Deletar a pasta `mobile/node_modules` e rodar `npm install` novamente para restaurar o estado anterior.