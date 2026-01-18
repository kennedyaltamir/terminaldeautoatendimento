# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 12:45:00
# 🧪 Checklist QA: MesaFlow Kiosk (L6)

## 1. Tela de Atração (Attract Screen)
- [ ] **Visual:** Fundo escuro (`bg-slate-950`), imagem com opacidade reduzida, partículas animadas.
- [ ] **Interação:** Toque em qualquer lugar da tela redireciona para o Menu.
- [ ] **Segurança:** Botão direito do mouse não abre menu de contexto. Seleção de texto bloqueada.
- [ ] **Responsividade:** Layout se adapta a Full HD (1920x1080) e Vertical (1080x1920).

## 2. Menu (Kiosk Mode)
- [ ] **Header:** Exibe botão "Voltar" grande, Logo e Badge "Autoatendimento Ativo".
- [ ] **Grid:** Produtos exibidos em cards grandes com alto contraste.
- [ ] **Carrinho:** Botão flutuante "Finalizar Pedido" aparece apenas quando há itens.
- [ ] **Inatividade:** Após 60s sem toque, modal "Ainda está aí?" aparece.
- [ ] **Reset:** Se modal de inatividade expirar (10s), carrinho é limpo e volta para Atração.

## 3. Checkout & Sucesso
- [ ] **Validação:** Tentar finalizar sem nome exibe erro (Toast).
- [ ] **Pagamento:** Seleção de método destaca visualmente a opção (Borda Laranja).
- **Sucesso:**
    - [ ] Ícone de Check animado.
    - [ ] Nome do cliente exibido em destaque.
    - [ ] Barra de progresso de auto-reset visível.
    - [ ] Redirecionamento automático para Atração após 10s.

## 4. Resiliência
- [ ] **Refresh:** Recarregar a página no meio do fluxo mantém o carrinho (se persistido) ou limpa corretamente (se volátil).
- [ ] **Offline:** Se a rede cair, o sistema não deve travar (fallback visual).

