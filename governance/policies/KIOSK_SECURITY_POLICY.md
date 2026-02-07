# 🖥️ Política de Segurança do Modo Kiosk (v14.0)
**Domain:** SECURITY / UX-HARDENING
**Status:** ENFORCED

## 1. Sandbox de Navegação e Trap Mode
O modo Kiosk atua como uma sandbox de hardware.
*   **Trap Mode:** Qualquer tentativa de fuga do modo Fullscreen ou detecção de perda de foco (Alt+Tab) dispara o rito de violação `BREACHED`.
*   **Lockdown:** O teclado virtual é a única entrada permitida. Atalhos de SO (F5, F11, Ctrl+R) são interceptados e anulados no nível do Kernel.

## 2. Theater Mode (Isolamento Operacional)
Durante a fase de checkout (`on_site` workflow), todos os elementos de branding periférico e navegação de suporte são removidos para eliminar distrações e erros de input.

## 3. Rito de Desbloqueio Administrativo
*   **Stealth Trigger:** O acesso ao painel de desbloqueio é oculto (exige sequência tátil nos 4 cantos da tela).
*   **Lockout Progressivo:** Erros de senha geram atrasos exponenciais (30s, 5m, 1h) para mitigar ataques de força bruta.

## 4. Persistência de Integridade
O estado do Kiosk é persistido em `MesaFlowDB (IndexedDB)`. Um refresh de página ou queda de energia não retira o sistema do modo `LOCKED`.
