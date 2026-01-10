# 🗣️ Teste Rápido: Comando de Voz no KDS

Como o seu ambiente já está rodando (`python run.py`) e você já gerou um pedido pago (`simular_pagamento.py`), siga os passos abaixo para validar a funcionalidade de voz.

## 1. Acesso ao KDS
1. Abra o navegador **Google Chrome** ou **Microsoft Edge** (O Firefox não suporta Web Speech API nativamente).
2. Acesse: [http://localhost:3000/admin/hamburgueria-ze/kitchen](http://localhost:3000/admin/hamburgueria-ze/kitchen)
3. Se pedir login:
   - **Email:** `admin@mesaflow.com`
   - **Senha:** `123456`

## 2. Ativação do Microfone
1. No canto superior direito do KDS, localize o botão com ícone de **Microfone** (ao lado do botão de Tela Cheia).
   - *Se o botão não aparecer, o navegador não suporta a API de voz.*
2. Clique no botão.
3. O navegador pedirá permissão para usar o microfone. Clique em **Permitir**.
4. O ícone deve mudar para um microfone **vermelho/pulsando** (Estado: Ouvindo).

## 3. Execução do Comando
1. Identifique o número do pedido que você acabou de criar na tela (ex: `#1234` ou `Mesa 1`).
2. Diga em voz alta e clara:
   
   > **"Pedido 1234 pronto"**
   
   ou (se for mesa):
   
   > **"Mesa 1 pronto"**

## 4. Validação
- **Visual:** O card do pedido deve se mover da coluna "Pendente/Preparando" para "Pronto" (Verde).
- **Feedback:** Um "Toast" (notificação preta) deve aparecer no topo da tela confirmando o comando reconhecido.
- **Console:** Pressione `F12` -> Aba `Console`. Você deve ver logs como:
  - `🎤 Voz detectada: pedido 1234 pronto`
  - `✅ Comando reconhecido`

## 5. Comandos Disponíveis
- "Pedido [X] pronto"
- "Pedido [X] finalizar"
- "Pedido [X] entregue"
- "Mesa [X] pronto"
