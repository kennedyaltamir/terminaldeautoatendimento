# DOMAIN: SECURITY
# LAST_MODIFIED: 2026-01-16 13:00:00
# 🔒 Protocolo de Segurança Kiosk (Lock Mode)
**Versão:** 1.0 | **Status:** ATIVO

## 1. Definição
O **Kiosk Lock Mode** é um estado de operação restrito que impede a saída do usuário da aplicação MesaFlow, garantindo a integridade do terminal de autoatendimento.

## 2. Mecanismos de Ativação
- **Gesto:** 5 toques rápidos no canto inferior direito.
- **Long Press:** Pressão contínua de 5 segundos no canto inferior direito.
- **Efeito:** Dispara `requestFullscreen()` e define flag `isLocked=true`.

## 3. Mecanismos de Proteção
1.  **Bloqueio de Contexto:** O evento `contextmenu` (botão direito) é interceptado globalmente.
2.  **Bloqueio de Seleção:** CSS `user-select: none` aplicado ao `body`.
3.  **Monitoramento de Fuga:** O evento `fullscreenchange` detecta saídas não autorizadas (ex: tecla ESC) e dispara imediatamente o Modal de Autenticação, bloqueando a UI até que a senha seja inserida.

## 4. Autenticação Administrativa
- **Senha Padrão:** `123456` (Deve ser alterada no setup).
- **Anti-Bruteforce:** 3 tentativas falhas bloqueiam o input por 30 segundos.
- **Feedback:** Haptic feedback e animação de "shake" em caso de erro.

## 5. Persistência
O estado de travamento é salvo no `localStorage`. Se o navegador for reiniciado (crash ou queda de energia), o sistema tentará restaurar o modo Kiosk automaticamente na próxima interação do usuário.

