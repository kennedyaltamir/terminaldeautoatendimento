# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 19:00:00
# 🖥️ Kiosk System Specification (L6)
**Status:** ACTIVE
**Version:** 2.0
**Authority:** MesaFlow Kernel
## 1. Visão Geral
O subsistema Kiosk (Totem) é uma interface de autoatendimento projetada para operar em modo quiosque (fullscreen), com proteções contra saída não autorizada e fluxo de compra simplificado.
## 2. Arquitetura de Estados (FSM)
O comportamento do Kiosk é governado por uma Máquina de Estados Finita (FSM) implementada no `KioskContext`.
### Estados
| Estado | Descrição | Gatilho de Entrada | Gatilho de Saída |
| :--- | :--- | :--- | :--- |
| `IDLE` | Estado inicial. Botão "ATIVAR MODO TOTEM" visível. | Boot do App. | Clique no botão de ativar. |
| `LOCKED` | Modo Totem ativo. Fullscreen forçado. Botão oculto. | Ação de ativar. | Violação de fullscreen ou sequência de desbloqueio. |
| `BREACHED` | Violação de segurança detectada (ESC/F11). Modal vermelho. | Saída de fullscreen sem senha. | Senha correta no modal. |
| `UNLOCKING` | Usuário iniciou sequência de desbloqueio (Stealth). | Sequência de toques (1-2-3-4). | Senha correta ou timeout. |
## 3. Fluxo de Segurança
### 3.1. Ativação
1.  Acesse `/[slug]/kiosk`.
2.  Clique em "ATIVAR MODO TOTEM".
3.  O navegador entra em Fullscreen.
4.  O estado muda para `LOCKED`.
5.  O botão desaparece.
### 3.2. Violação (Trap Mode)
1.  Usuário pressiona ESC ou F11.
2.  Evento `fullscreenchange` detecta saída.
3.  Estado muda para `BREACHED`.
4.  Modal de "VIOLAÇÃO DE SEGURANÇA" bloqueia a tela.
5.  Única saída: Senha Mestre.
### 3.3. Desbloqueio (Stealth Trigger)
1.  Toque nos 4 cantos da tela em sentido horário (Top-Left -> Top-Right -> Bottom-Right -> Bottom-Left).
2.  Modal de Senha aparece (Estado `UNLOCKING`).
3.  Senha correta -> Estado `IDLE` (Botão reaparece).
## 4. Persistência
- O estado é salvo no `localStorage` (`mesaflow_kiosk_state`).
- Se a página for recarregada em `LOCKED` ou `BREACHED`, ela retorna a esse estado imediatamente.
## 5. Integração com Carrinho
- O Kiosk usa o mesmo `CartContext` do menu normal.
- Diferença: O carrinho é limpo automaticamente após X segundos de inatividade (Idle Timer).

