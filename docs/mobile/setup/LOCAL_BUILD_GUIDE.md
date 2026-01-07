# 🏗️ Guia de Build Local (Android Studio + VS Code)

Este guia descreve como gerar o APK utilizando os recursos da sua máquina local, integrando o fluxo do Expo com o Android Studio.

## 1. O Conceito de Prebuild
No Expo Managed Workflow, a pasta `android` não deve ser editada manualmente na maioria dos casos. Ela é **gerada** a partir do `app.json`.
Para abrir no Android Studio, precisamos materializar essa pasta.

## 2. Passo a Passo

### Passo 1: Gerar o Código Nativo (VS Code)
No terminal do VS Code, dentro da pasta `mobile/`:

```bash
# 1. Limpa builds anteriores e gera a pasta android/ fresca
npx expo prebuild --platform android --clean
```

*O que isso faz:* Cria a pasta `mobile/android` com todo o código Java/Kotlin e configurações do Gradle baseadas no seu `app.json`.

### Passo 2: Abrir no Android Studio
1.  Abra o **Android Studio**.
2.  Clique em **Open**.
3.  Navegue até a pasta `.../mesaflow/mobile/android` (Importante: Selecione a pasta `android`, não a `mobile`).
4.  Aguarde o **Gradle Sync** finalizar (pode demorar na primeira vez enquanto baixa dependências).

### Passo 3: Gerar o APK (Assinado para Debug/Preview)

**Opção A: Via Linha de Comando (Mais rápido)**
No terminal do VS Code (pasta `mobile/android`):
```bash
# Windows
cd android
./gradlew assembleRelease

# Mac/Linux
cd android
./gradlew assembleRelease
```

**Opção B: Via Interface do Android Studio**
1.  No menu superior, vá em **Build** > **Build Bundle(s) / APK(s)** > **Build APK(s)**.
2.  O Android Studio notificará quando terminar.
3.  Clique em **locate** na notificação para abrir a pasta do APK.

## 3. Onde fica o APK?
Após o build, o arquivo estará em:
`mobile/android/app/build/outputs/apk/release/app-release.apk`

## 4. Solução de Problemas Comuns

### Erro: "SDK Location not found"
Crie um arquivo `local.properties` dentro de `mobile/android/` com o caminho do seu SDK:
```properties
sdk.dir=C\:\\Users\\SEU_USUARIO\\AppData\\Local\\Android\\Sdk
```
*(Nota: O `npx expo prebuild` geralmente cria isso automaticamente, mas verifique se falhar).*

### Erro: "Java Heap Space"
Se o build falhar por falta de memória, edite `mobile/android/gradle.properties`:
```properties
org.gradle.jvmargs=-Xmx4096m -XX:MaxMetaspaceSize=512m
```

---
**Atenção:** Sempre que você instalar uma nova biblioteca nativa (ex: câmera, impressora) ou mudar o `app.json`, você deve rodar `npx expo prebuild` novamente.
