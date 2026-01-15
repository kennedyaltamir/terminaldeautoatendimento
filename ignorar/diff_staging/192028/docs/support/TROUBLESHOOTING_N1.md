# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-14 19:30:00

# 📞 Guia de Suporte Nível 1 (Helpdesk)

Este guia é destinado aos atendentes de suporte para resolução rápida de problemas comuns reportados pelos clientes via WhatsApp.

---

## 1. Problemas de Impressão

**Cliente:** "A impressora parou de imprimir os pedidos."

1.  **Verificar App:** Peça para o cliente abrir o App MesaFlow no tablet/celular.
2.  **Tela de Debug:** Vá em Menu > Configurações > Debug de Impressora.
3.  **Teste:** Clique em "Imprimir Teste".
    *   *Imprimiu?* O problema pode ser no backend (WebSocket desconectado). Peça para recarregar a página.
    *   *Não imprimiu?* Verifique se o Bluetooth está ligado e a impressora pareada.
4.  **RawBT:** Verifique se o app "RawBT" está instalado e configurado como serviço.

---

## 2. Problemas de Cardápio

**Cliente:** "Alterei o preço mas não mudou no cardápio digital."

1.  **Cache:** O cardápio usa cache de 5 minutos para performance.
2.  **Ação:** Peça para o cliente aguardar 5 minutos ou abrir em aba anônima.
3.  **Forçar:** No Painel Admin, salvar o produto novamente força a invalidação do cache.

---

## 3. Problemas de Login

**Cliente:** "Não consigo entrar, diz senha inválida."

1.  **Reset:** Envie o link de "Esqueci minha senha" (`/admin/forgot-password`).
2.  **Verificação:** Confirme se o cliente está usando o e-mail de cadastro (Owner) e não um e-mail de funcionário desativado.

---

## 4. Pedidos não aparecem na Cozinha (KDS)

**Cliente:** "O cliente pediu mas a tela da cozinha está vazia."

1.  **Conexão:** Verifique se há um ícone de "Wifi Cortado" ou "Offline" no topo da tela da cozinha.
2.  **Filtro:** Verifique se a cozinha não está filtrada por "Bar" ou "Sobremesa" (abas superiores).
3.  **Refresh:** Pressione `F5` ou arraste para baixo (mobile) para forçar uma sincronização completa.

---
*MesaFlow Support Team*
