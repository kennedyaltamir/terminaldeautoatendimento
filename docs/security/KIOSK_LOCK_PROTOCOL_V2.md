# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-16 13:45:00
# 🔒 Protocolo de Segurança Kiosk (Lock Mode v2.1)
**Versão:** 2.1 (Production Grade) | **Status:** ATIVO

## 1. Máquina de Estados de Segurança (FSM)
O sistema opera sob uma FSM estrita gerenciada pelo `KioskContext`:
- **IDLE:** Modo de manutenção/setup. Interface desbloqueada.
- **LOCKED:** Modo de operação. Fullscreen ativo. Saída bloqueada.
- **BREACHED:** Estado de violação (Trap Mode). Fullscreen perdido sem autorização. UI bloqueada por modal vermelho.
- **UNLOCKING:** Modal de senha ativo.

## 2. Contrato de Erro e Validação
A função `validateAndUnlock` retorna um objeto tipado `UnlockResult`:
- `ok: true` -> Desbloqueio autorizado.
- `ok: false` -> Motivo:
    - `INVALID_PASSWORD`: Senha incorreta (Gera Shake + Vibração).
    - `LOCKED_OUT`: Bloqueio temporário por tentativas excessivas.
    - `NETWORK_ERROR`: Falha de comunicação com backend (Futuro).

## 3. Fonte da Verdade (Source of Truth)
- **Estado de Bloqueio:** O `KioskContext` é a autoridade máxima. O `localStorage` é apenas um mecanismo de persistência entre reloads.
- **Lockout Timer:** O tempo de bloqueio é calculado no momento da tentativa (`Date.now() > lockoutEndTime`). O timer visual no modal é apenas informativo.

## 4. Proteção contra Violação (The Trap)
Se o navegador perder o foco ou sair do modo tela cheia (ex: Alt+Tab, F11, Crash de Driver) enquanto estiver no estado `LOCKED`:
1. O estado muda imediatamente para `BREACHED`.
2. O `KioskExitAuthModal` é renderizado em modo de emergência (Borda Vermelha).
3. O botão "Cancelar" é removido.
4. **Limitação Conhecida:** Se o navegador bloquear a reentrada automática em Fullscreen (ex: falta de gesto do usuário), o sistema permanece em `BREACHED` até que uma senha válida seja inserida, momento em que o operador pode restaurar o Fullscreen manualmente.

## 5. Auditoria
Todas as tentativas de desbloqueio (sucesso ou falha) devem ser registradas no `AuditLog` do backend.

