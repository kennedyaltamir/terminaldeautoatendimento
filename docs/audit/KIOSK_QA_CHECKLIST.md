# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 19:00:00
# ✅ Checklist de QA: Kiosk Mode (L6)
## 1. Tela de Atração (Attract Screen)
- [ ] **Rota:** `/[slug]/kiosk`
- [ ] **Visual:** Background com vídeo/imagem de alta qualidade.
- [ ] **Texto:** "TOQUE PARA COMEÇAR" pulsante.
- [ ] **Interação:** Qualquer toque na tela redireciona para `/[slug]/menu?kiosk=true`.
- [ ] **Botão Ativar:** Visível apenas em estado `IDLE`.
## 2. Modo Bloqueado (LOCKED)
- [ ] **Ativação:** Clicar em "ATIVAR MODO TOTEM" entra em fullscreen.
- [ ] **Persistência:** Recarregar a página (F5) mantém o fullscreen (se o navegador permitir) ou re-exige interação, mas mantém estado lógico `LOCKED`.
- [ ] **Botão:** O botão "ATIVAR" deve desaparecer.
## 3. Violação (BREACHED)
- [ ] **Gatilho:** Pressionar ESC.
- [ ] **Reação:** Modal vermelho "VIOLAÇÃO DE SEGURANÇA" aparece imediatamente.
- [ ] **Bloqueio:** Não é possível fechar o modal clicando fora ou em "Cancelar".
- [ ] **Recuperação:** Digitar senha correta restaura o sistema.
## 4. Desbloqueio Administrativo
- [ ] **Gatilho:** Sequência de toques nos 4 cantos.
- [ ] **Modal:** Modal de senha padrão (Azul/Cinza).
- [ ] **Senha Errada:** Feedback visual "SENHA INCORRETA".
- [ ] **Senha Certa:** Retorna ao estado `IDLE`.
## 5. Fluxo de Pedido (Kiosk Mode)
- [ ] **Carrinho:** Adicionar item.
- [ ] **Inatividade:** Aguardar 60s (ou tempo configurado). Modal de "Ainda está aí?" aparece.
- [ ] **Timeout:** Se não responder, carrinho limpa e volta para Attract Screen.

