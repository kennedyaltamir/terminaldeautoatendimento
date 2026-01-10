# 📱 Guia de Teste Mobile: Android Studio & APK
Este guia detalha como compilar, instalar e validar as funcionalidades da TASK-MOB-02 utilizando o seu ambiente Android Studio.

---

## 1. Preparação do Ambiente (Checklist)
Antes de gerar o APK, garanta que:
1. **Java JDK 17:** Verifique com `java -version`. É a versão exigida pelo React Native 0.76.
2. **Android SDK:** No Android Studio, vá em *SDK Manager* e garanta que o "Android SDK Platform 34 ou 35" está instalado.
3. **Variáveis de Ambiente:** `ANDROID_HOME` deve apontar para sua pasta do SDK e `%ANDROID_HOME%\platform-tools` deve estar no seu PATH.

---

## 2. Método Rápido: Teste via Emulador (Sem gerar APK)
Se você quer apenas ver as telas agora, não precisa gerar o APK final.
1. Abra o **Android Studio** e inicie um **Virtual Device (AVD)**.
2. No terminal da raiz do projeto:
   ```bash
   cd mobile
   npm install
   npx expo start
   ```
3. Pressione a tecla **`a`** no terminal. O Expo irá instalar o "Expo Go" no emulador e abrir o MesaFlow automaticamente.

---

## 3. Método Completo: Gerando o APK Local (EAS Build)
Para gerar um arquivo `.apk` real para instalar no emulador ou celular físico:

1. **Instale o EAS CLI:**
   ```bash
   npm install -g eas-cli
   ```
2. **Faça o Build Local (Requer Docker ou WSL2 no Windows):**
   ```bash
   cd mobile
   eas build --platform android --profile preview --local
   ```
   *Nota: O perfil `preview` em `eas.json` está configurado para gerar APK em vez de AAB (loja).*

3. **Instalação no Emulador:**
   Após o término, arraste o arquivo `.apk` gerado para dentro da tela do emulador do Android Studio.

---

## 4. Roteiro de Testes (Passo a Passo)

### Teste 1: Boot e Assets
- **Ação:** Abra o aplicativo.
- **Comportamento:** Você deve ver a Splash Screen (fundo escuro com logo) por alguns segundos. Não deve haver erros de "Image not found".
- **Sucesso:** O app abre na tela de Login.

### Teste 2: Autenticação (Mock)
- **Ação:** Na tela de login, insira qualquer e-mail e senha. Clique em **"Entrar"**.
- **Comportamento:** O botão utiliza a lógica de `login('fake-token', { role: 'waiter' })` implementada no `LoginScreen.tsx`.
- **Sucesso:** O app transita instantaneamente para o Dashboard.

### Teste 3: Navegação por Cargo (Simulação)
Como o login atual está fixo para teste, para ver os outros cargos, você pode alterar temporariamente o arquivo `mobile/src/screens/auth/LoginScreen.tsx`:

- **Para ver Cozinha:** Mude para `login('fake-token', { role: 'kitchen' });`
- **Para ver Entregador:** Mude para `login('fake-token', { role: 'driver' });`

**O que validar em cada um:**
1. **Garçom:** Verifique se o grid de mesas aparece com os status (Verde/Laranja/Vermelho).
2. **Cozinha:** Verifique se a lista de pedidos mostra os itens (ex: 2x X-Bacon) e as bordas coloridas de status.
3. **Entregador:** Verifique se o card de entrega mostra o endereço e o botão "Iniciar Rota".

### Teste 4: Persistência de Sessão
- **Ação:** Com o app logado, feche-o completamente (mate o processo no Android). Abra o app novamente.
- **Comportamento:** O `App.tsx` chama o `hydrate()` do `auth.store.ts`, que busca o token no `SecureStore`.
- **Sucesso:** O app deve abrir direto no Dashboard, pulando a tela de login.

---

## 5. Troubleshooting (Solução de Problemas)
- **Erro de Conexão:** Se o app não carregar dados da API (futuro), garanta que o seu `.env` aponta para o IP da sua máquina (ex: `192.168.x.x`) e não `localhost`, pois o emulador enxerga o `localhost` como ele mesmo.
- **Metro Bundler travado:** Rode `npx expo start --clear`.

---
*Manual gerado para MesaFlow v3.5 - Janeiro 2026*
