# 📱 Detalhamento Técnico: Build Mobile de Produção (TASK-GTM-03)

## 1. Contexto
O app atual é compilado como APK (Android Package) para testes locais. As lojas (Google Play e App Store) exigem formatos otimizados e assinados digitalmente.

## 2. Especificação de Implementação

### 2.1 Configuração EAS (`eas.json`)
Definir o perfil `production` estrito:
```json
"production": {
  "channel": "production",
  "autoIncrement": true,
  "android": {
    "buildType": "app-bundle" // Gera .aab em vez de .apk
  },
  "ios": {
    "resourceClass": "m1-medium" // Build mais rápido
  }
}
```

### 2.2 Metadados (`app.json`)
- **Versionamento:** Garantir que `version` segue SemVer (ex: 1.0.0) e `versionCode`/`buildNumber` são inteiros incrementais.
- **Permissões:** Revisar `android.permissions`. Remover permissões não usadas (ex: Acesso a contatos, SMS) para evitar rejeição na loja.
- **Assets:** Validar se `icon.png` (1024x1024) e `adaptive-icon.png` estão presentes e sem transparência (requisito Apple).

### 2.3 Assinatura (Signing)
- Utilizar o **EAS Credentials** para gerenciar Keystores (Android) e Certificates/Provisioning Profiles (iOS).
- Não commitar chaves no repositório.

## 3. Plano de Validação
1.  Executar `eas build --platform android --profile production --local` (ou cloud).
2.  Verificar se o arquivo gerado é um `.aab`.
3.  Tentar subir o `.aab` no "Internal Testing" do Google Play Console (validação estática da loja).
