
# 🧪 Plano de Verificação: TASK-MOB-FIX-01

## 1. Critérios de Sucesso (DoD)
- [ ] Script `scripts/maintenance/mobile_doctor.py` retorna "HEALTHY" para todos os checks.
- [ ] O comando `npx expo start` inicia o Metro Bundler sem erros fatais.
- [ ] O aplicativo pode ser visualizado no Expo Go ou simulador.

## 2. Procedimento de Teste
1. Executar `python scripts/maintenance/mobile_doctor.py`.
2. Tentar rodar `cd mobile && npx expo start --clear`.
3. Validar se o QR Code do Expo é gerado no terminal.