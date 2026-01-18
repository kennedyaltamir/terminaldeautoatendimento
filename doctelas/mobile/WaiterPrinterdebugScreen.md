# 🖨️ WaiterPrinterdebugScreen
> **Plataforma:** MOBILE | **Domínio:** HARDWARE | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Ferramenta de diagnóstico e homologação de hardware. Permite que a equipe de suporte e o lojista testem a conectividade Bluetooth e a compatibilidade de comandos ESC/POS com impressoras térmicas locais.

## 2. Estrutura Técnica
- **Device Scanner:** Lista de dispositivos Bluetooth pareados e disponíveis no alcance.
- **Command Console:** Logs em tempo real dos bytes enviados para a impressora.
- **Test Suite:** Botões pré-configurados para testes de alinhamento, fontes e corte.

## 3. Elementos Interativos
- **Scan Devices:** Dispara a busca por novos periféricos via `react-native-ble-plx`.
- **Print Test Page:** Envia um buffer padrão contendo texto, negrito e um QR Code de teste.
- **Open Drawer:** Envia o comando de pulso elétrico para abertura de gaveta de dinheiro.

## 4. Regras de Homologação
- **Encoding Check:** Validação de caracteres especiais (acentuação) no padrão Latin-1.
- **Width Detection:** Configuração entre bobinas de 58mm (32 colunas) e 80mm (48 colunas).
- **Connection Persistence:** Opção de "Salvar como Padrão" para reconexão automática no boot.

## 5. Estados da Tela
- **Searching:** Animação de radar durante o escaneamento Bluetooth.
- **Connected:** Indicador verde com o nome e endereço MAC do hardware ativo.
- **Error:** Diagnóstico de falhas comuns (Bluetooth desligado, sem permissão de GPS).

## 6. Fluxo de Hardware
1. App solicita permissão de `BLUETOOTH_CONNECT`.
2. Usuário seleciona a impressora.
3. `PrinterService` estabelece o socket RFCOMM e envia o stream binário.

---
*MesaFlow Mobile Kernel v5.0*

