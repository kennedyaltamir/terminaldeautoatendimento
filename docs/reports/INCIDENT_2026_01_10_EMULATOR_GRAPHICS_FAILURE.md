# 🚨 Relatório de Incidente: Falha de Renderização e Boot na API 36

**Data:** 10 de Janeiro de 2026  
**Sintoma:** O emulador reporta "Boot Completed", mas a tela permanece preta. Erros críticos de `opengl32sw` e `UpdateLayeredWindowIndirect` detectados nos logs.

## 1. Diagnóstico Técnico (Root Cause Analysis)
Seus logs revelam uma falha na ponte entre a sua GPU (RTX 3060) e o driver de vídeo do Android 15/16 (API 36).

### Evidências nos Logs:
1. `Critical: Failed to load opengl32sw`: O emulador tentou usar a renderização por software como fallback e falhou porque a biblioteca não foi encontrada no path do SDK.
2. `Guest Angle is still unstable for API > 35`: Você está usando uma versão "Preview" do Android que tem incompatibilidade conhecida com o motor ANGLE (que traduz OpenGL para DirectX no Windows).
3. `UpdateLayeredWindowIndirect failed`: Erro de interface do Windows. O emulador não consegue desenhar a janela do dispositivo na sua área de trabalho devido a um conflito de buffer de vídeo.

## 2. As 5 Possibilidades de Falha

### 2.1. Incompatibilidade da API 36 (Vanilla Ice Cream)
A API 36 é experimental. Em muitos hardwares Windows, o subsistema gráfico do Android 15/16 ainda não consegue inicializar o `SurfaceFlinger` (gerenciador de tela do Android) corretamente em emuladores.

### 2.2. Falha no Handshake Vulkan/OpenGL
O log mostra `WARNING | Please update the emulator to one that supports VulkanVirtualQueue`. Sua RTX 3060 suporta Vulkan 1.4, mas o emulador não consegue criar a fila virtual de renderização, travando o frame buffer.

### 2.3. Conflito de DPI/Resolução
O erro `UpdateLayeredWindowIndirect` ocorre frequentemente quando há um descasamento entre a escala do Windows (ex: 125% ou 150%) e a resolução do AVD (1080x2400).

### 2.4. Corrupção do Cache de Sombras (Shaders)
O emulador armazena shaders compilados da sua GPU. Se houve uma atualização de driver da NVIDIA recentemente, os shaders antigos causam tela preta.

### 2.5. Limitação do EAS Build Local no Windows
O erro `Unsupported platform, macOS or Linux is required` confirma que você não pode gerar o APK localmente via `eas build --local` no Windows nativo (exige WSL2). Isso impede que você teste um binário real, forçando o uso do Expo Go, que é mais sensível a erros de renderização.

## 3. Plano de Resolução
1. Executar o script `scripts/diagnosis/emulator_deep_fix.py`.
2. Criar um dispositivo com **API 34 (Android 14)**, que é a versão estável recomendada.
3. Usar o build em nuvem da Expo para gerar o APK.
