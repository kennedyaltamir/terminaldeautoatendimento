# 📺 Guia do Monitor Público de Pedidos (Public Monitor)

O Monitor Público é uma interface de alta visibilidade projetada para ser exibida em TVs ou monitores voltados para o cliente no salão ou balcão de retirada.

## 1. Acesso
A URL segue o padrão de rotas públicas do MesaFlow:
`http://localhost:3000/[SLUG]/monitor`

**Exemplo Local:** [http://localhost:3000/hamburgueria-ze/monitor](http://localhost:3000/hamburgueria-ze/monitor)

## 2. Comportamento Visual
A tela é dividida em duas zonas principais de status:

### 🟠 Coluna "Preparando" (Esquerda)
- Exibe pedidos com status `pending`, `accepted` ou `preparing`.
- Os números são exibidos em cinza/laranja para indicar que a produção está em curso.
- Animação de entrada suave (fade-in).

### 🟢 Coluna "Pronto para Retirada" (Direita)
- Exibe pedidos com status `ready`.
- **Destaque Máximo:** Os cards possuem bordas brilhantes e uma animação de pulso contínua.
- **Alerta Sonoro:** O sistema emite um sinal sonoro ("Ding") sempre que um pedido transita para esta coluna.

## 3. Especificações Técnicas
- **Real-time:** Utiliza WebSockets para garantir latência zero. Assim que o cozinheiro clica em "Pronto" no KDS, o número aparece no telão.
- **Identificação:** Exibe os 4 últimos dígitos do ID do pedido (Display ID) e o nome do cliente.
- **Auto-ajuste:** O layout é responsivo, mas otimizado para visualização em 1080p (Full HD).

## 🛠️ Dica de Instalação
Para uso profissional, utilize um navegador em **Modo Quiosque** (Chrome Kiosk Mode) para ocultar barras de ferramentas e cursores do mouse.
