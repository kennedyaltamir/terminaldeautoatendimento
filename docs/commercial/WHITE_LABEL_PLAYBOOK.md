
# ⚪ White-Label Playbook: Escalando a Marca do Cliente

O MesaFlow permite que grandes redes operem com sua própria identidade visual.

## 1. Estratégia de Build
Para gerar um app com a marca do cliente (ex: "App do Burger King"):
1. **Assets:** Substituir a pasta `mobile/assets/` pelas imagens do cliente.
2. **Config:** Alterar `name` e `slug` em `app.json`.
3. **EAS:** Criar um novo `projectId` no Expo para o cliente.

## 2. Injeção de Variáveis
Utilizar o comando de build com as variáveis do cliente:
```bash
EXPO_PUBLIC_API_URL="https://api.cliente.com.br" \
EXPO_PUBLIC_PRIMARY_COLOR="#FF0000" \
eas build --platform android
```

## 3. Publicação
- **Opção A:** Publicar na conta do MesaFlow (Multitenant).
- **Opção B:** Publicar na conta do Cliente (Custom Build).

---

