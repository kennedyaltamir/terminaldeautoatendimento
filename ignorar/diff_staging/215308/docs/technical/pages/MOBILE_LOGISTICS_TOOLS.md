# 📱 Módulo Mobile: Logística e Ferramentas
**Telas:** `DriverDashboard` | `PrinterDebugScreen`

## 1. DriverDashboard (App do Entregador)
- **Intenção:** Gestão de rotas de delivery.
- **Elementos:**
    - **Map Integration:** Botão para abrir Waze/Google Maps com o destino.
    - **POD (Proof of Delivery):** Campo para código de 4 dígitos do cliente.
- **Comportamento:** Captura GPS em background (se permitido) para rastreio do cliente.

## 2. PrinterDebugScreen (Suporte Técnico)
- **Intenção:** Homologação de hardware em campo.
- **Elementos:** Lista de dispositivos Bluetooth pareados, Botão "Imprimir Teste".
- **Comportamento:** Envia buffer ESC/POS bruto para validar alinhamento e corte.
