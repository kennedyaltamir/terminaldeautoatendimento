# Script de Atualização Rápida do App no Emulador
$ADB = "C:\Users\Kennedy Oliveira\AppData\Local\Android\Sdk\platform-tools\adb.exe"
$PACKAGE = "com.mesaflow.mobile"

# 1. Localizar o APK mais recente na pasta de Downloads
$APK = Get-ChildItem -Path "$env:USERPROFILE\Downloads" -Filter "application-*.apk" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($null -eq $APK) {
    Write-Host "❌ Nenhum APK encontrado em Downloads." -ForegroundColor Red
    exit
}

Write-Host "📦 Atualizando para o APK: $($APK.Name)" -ForegroundColor Cyan

# 2. Remover versão antiga
Write-Host "🧹 Removendo versão antiga..."
& $ADB uninstall $PACKAGE

# 3. Instalar nova versão
Write-Host "🚀 Instalando nova versão..."
& $ADB install $APK.FullName

Write-Host "✨ Concluído! Abra o app no emulador." -ForegroundColor Green
