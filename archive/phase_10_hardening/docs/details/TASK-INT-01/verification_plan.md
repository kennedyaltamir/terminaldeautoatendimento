# 🧪 Plano de Verificação: TASK-INT-01

## 1. Critérios de Sucesso (DoD)
- [ ] Manual de integrações atualizado com prints ou passos claros.
- [ ] Script `scripts/production/validate_integrations.py` atualizado para testar os novos campos.
- [ ] O sistema identifica se uma integração está "Parcial" ou "Completa" no painel admin.

## 2. Procedimento de Teste
1. Seguir o manual para configurar uma conta de teste (Sandbox).
2. Rodar o script de validação de conectividade.
3. Verificar se o backend loga corretamente o recebimento de um ping de webhook simulado.
