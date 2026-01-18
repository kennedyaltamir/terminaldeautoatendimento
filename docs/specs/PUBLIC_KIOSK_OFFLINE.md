# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 12:30:00
# 📺 Módulo: Totem & Fallbacks
**Rotas:** `/[slug]/kiosk` | `/offline`

## 1. Totem (Kiosk Mode)
- **Intenção:** Autoatendimento em terminais físicos.
- **Elementos:** Vídeo de fundo em alta definição, Botão "Toque para Iniciar".
- **Comportamento:** 
    - Bloqueia o menu de contexto (botão direito).
    - Inatividade de 60s dispara o `InactivityModal`.
    - Se não houver resposta, reseta o carrinho e volta para a tela de atração.

## 2. Página Offline
- **Intenção:** Manter a confiança do usuário durante falhas de rede.
- **Elementos:** Animação de busca de sinal, Botão "Tentar Novamente".
- **Comportamento:** Tenta realizar um `ping` na API a cada 5 segundos para auto-recuperação.

