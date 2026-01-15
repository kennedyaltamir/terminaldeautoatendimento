
# 🌍 Configuração de Ambiente Mobile (EAS & Local)

Este documento define o padrão de configuração de variáveis de ambiente para o aplicativo MesaFlow Mobile, garantindo segurança e conformidade com as lojas (Apple/Google).

## 1. Arquitetura de Configuração

O projeto utiliza `expo-constants` e injeção de variáveis em tempo de build.
**NUNCA** commite arquivos `.env` contendo chaves de produção.

### Arquivo Central: `mobile/src/config/env.ts`
Este arquivo é o único ponto de verdade para URLs e chaves. Ele valida:
- Existência de variáveis críticas.
- Uso de HTTPS em produção.
- Fallbacks seguros apenas em modo `__DEV__`.

## 2. Desenvolvimento Local

Para rodar localmente, crie um arquivo `.env` na raiz da pasta `mobile/`:

```ini
# mobile/.env
EXPO_PUBLIC_API_URL=http://192.168.1.X:8000/api
EXPO_PUBLIC_WS_URL=ws://192.168.1.X:8000/ws
EXPO_PUBLIC_ENV=development
EXPO_PUBLIC_ENABLE_LOGS=true
```

> **Nota:** Substitua `192.168.1.X` pelo IP da sua máquina na rede local. Não use `localhost` se estiver testando em dispositivo físico.

## 3. Produção (EAS Build)

Para builds de produção, as variáveis devem ser configuradas no **EAS Secrets** ou no `eas.json` (apenas para variáveis não sensíveis).

### Configuração via `eas.json` (Recomendado para URLs públicas)

```json
{
  "build": {
    "production": {
      "env": {
        "EXPO_PUBLIC_API_URL": "https://api.mesaflow.com.br/api",
        "EXPO_PUBLIC_WS_URL": "wss://api.mesaflow.com.br/ws",
        "EXPO_PUBLIC_ENV": "production"
      }
    }
  }
}
```

## 4. Auditoria de Segurança

Antes de qualquer deploy, execute o script de auditoria para garantir que nenhum IP de desenvolvimento vazou para o código fonte:

```bash
python scripts/maintenance/env_production_audit.py
```

## 5. Checklist de Release

- [ ] `EXPO_PUBLIC_API_URL` usa `https://`.
- [ ] `EXPO_PUBLIC_WS_URL` usa `wss://`.
- [ ] `EXPO_PUBLIC_ENV` está definido como `production`.
- [ ] Logs de debug desativados (`ENABLE_LOGS=false`).

