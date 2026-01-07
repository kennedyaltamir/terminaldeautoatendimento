# 1. Adicionar as mudanças no package.json e lockfile
git add .

# 2. Commit de alinhamento de dependências
git commit -m "fix(mobile): align dependencies with SDK 54 and resolve peer conflicts"

# 3. Enviar para o repositório (Opcional, mas recomendado)
git push origin main

# 4. Disparar o build real no EAS
cd mobile
eas build --profile preview --platform android
