# 📱 Módulo Mobile: Autenticação e Cozinha (KDS)
**Telas:** `LoginScreen` | `OrdersScreen`

## 1. LoginScreen (Acesso Operacional)
- **Intenção:** Entrada segura para staff com persistência em hardware.
- **Elementos:**
    - **AuthInput (E-mail/Senha):** Com validação de tipos.
    - **SecureStore Integration:** Salva JWT em área criptografada do chip.
- **Comportamento:** 
    - Se o token expirar, o `AuthGate` intercepta e redireciona para cá.
    - Suporta biometria (FaceID/Digital) se configurado.

## 2. OrdersScreen (Monitor de Produção Nativo)
- **Intenção:** Gestão de fila de preparo em tablets/celulares.
- **Elementos:**
    - **FlashList:** Lista de alta performance (60 FPS) para centenas de pedidos.
    - **SLA Timer:** Cronômetro reativo que muda a cor do card (Verde/Amarelo/Vermelho).
    - **Vibration Engine:** Dispara pulsos táteis em novos pedidos.
- **Comportamento:**
    - **WebSocket Sync:** Atualiza status sem necessidade de pull-to-refresh.
    - **Offline-First:** Exibe últimos pedidos mesmo sem rede.
- **API:** `GET /api/admin/[slug]/orders`.
