# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-14 18:15:00

# 🧪 Roteiro de Teste Funcional Manual
**Instruções:** Para cada página, tente realizar as ações principais. Se algo não funcionar como esperado, anote na coluna "Observações/Erros".

---

## 1. ÁREA PÚBLICA (Cliente Final)

| Página | Ação Testada | Resultado Esperado | Funcionou? | Observações/Erros |
| :--- | :--- | :--- | :---: | :--- |
| **Landing Page** (`/`) | Clicar em "Começar Agora" | Ir para `/admin/register` | [ ] | |
| **Menu Digital** (`/[slug]/menu`) | Adicionar item ao carrinho | Item aparecer no rodapé | [ ] | |
| | Finalizar Pedido (Checkout) | Pedido ser criado e ir para tela de status | [ ] | |
| **Kiosk** (`/[slug]/kiosk`) | Tocar na tela | Ir para o Menu em modo Kiosk | [ ] | |
| **Monitor** (`/[slug]/monitor`) | (Passivo) | Mostrar pedidos "Preparando" e "Pronto" | [ ] | |

---

## 2. ÁREA ADMINISTRATIVA (Gestão)

| Página | Ação Testada | Resultado Esperado | Funcionou? | Observações/Erros |
| :--- | :--- | :--- | :---: | :--- |
| **Login** (`/admin/login`) | Entrar com credenciais | Redirecionar para Dashboard | [ ] | |
| **Dashboard** (`.../dashboard`) | Visualizar gráficos | Dados carregados (não zerados) | [ ] | |
| **Mesas** (`.../tables`) | Criar nova mesa | Mesa aparecer na lista e gerar QR Code | [ ] | |
| **Cardápio** (`.../menu`) | Criar Categoria | Categoria aparecer na lista | [ ] | |
| | Criar Produto | Produto aparecer na lista | [ ] | |
| **Estoque** (`.../inventory`) | Adicionar Ingrediente | Ingrediente salvo no banco | [ ] | |

---

## 3. ÁREA OPERACIONAL (Tempo Real)

| Página | Ação Testada | Resultado Esperado | Funcionou? | Observações/Erros |
| :--- | :--- | :--- | :---: | :--- |
| **Cozinha (KDS)** (`.../kitchen`) | Receber Pedido | Pedido novo aparecer sozinho (WebSocket) | [ ] | |
| | Avançar Status | Pedido mudar de cor/coluna | [ ] | |
| **Garçom (POS)** (`.../waiter`) | Abrir Mesa | Status da mesa mudar para "Ocupada" | [ ] | |
| | Lançar Pedido | Pedido ir para a Cozinha | [ ] | |
| | Fechar Conta | Gerar total e QR Code Pix | [ ] | |
| **Expedição** (`.../expeditor`) | Ver Prontos | Ver pedidos marcados como "Pronto" | [ ] | |
| **Delivery** (`.../delivery`) | Despachar | Atribuir entregador e mudar status | [ ] | |

---

## 4. RESUMO GERAL
**Qual a funcionalidade mais crítica que não está funcionando hoje?**
> (Escreva aqui...)

**Nota Geral (0-10):**
> (___)

