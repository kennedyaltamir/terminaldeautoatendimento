# 🖥️ Especificação Técnica: TASK-FEAT-01
> **Título:** Modo Totem com Descanso de Tela
> **Status:** SPECIFIED

## 1. Comportamento do Totem (Kiosk)
- **Interface:** Travada em tela cheia (Fullscreen API).
- **Navegação:** Sem barra de endereços ou botões de "voltar" do sistema.
- **Timeout de Inatividade:** Após 60 segundos sem toque, o sistema limpa o carrinho e volta para a tela inicial.

## 2. Descanso de Tela (Screensaver)
- **Ativação:** Após 2 minutos de inatividade.
- **Visual:** Carrossel de imagens de alta qualidade dos produtos em destaque ou vídeos curtos.
- **Ação:** "Toque para começar" interrompe o descanso e abre o menu.

## 3. Requisitos Técnicos
- Hook `useIdleTimer` para monitoramento de eventos de mouse/touch.
- Componente `ScreensaverOverlay` com animações de transição suave.
