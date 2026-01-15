
# 🧪 Matriz de Testes Human-Like (L5) - MesaFlow Mobile

**Status:** ATIVO
**Executor:** Maestro + Optimus Kernel
**Objetivo:** Simular comportamento humano para validação visual e funcional antes do Production Lock.

## 🔹 CATEGORIA A — BOOT / CONTEXTO (Infraestrutura)
| ID | Nome | Ação Humana Simulada | Critério de Sucesso |
|:---|:---|:---|:---|
| **T01** | Cold Start | Matar o app e abrir do zero. | Splash screen some em < 2s, Home carrega sem flash branco. |
| **T02** | Hot Reload / Resume | Minimizar app, abrir outro app, voltar em 5s. | Estado da tela mantido, sem reload completo. |
| **T03** | Offline Boot | Ativar modo avião, abrir app. | Tela de "Sem Conexão" ou Cache visível. Não trava no splash. |
| **T04** | Crash Recovery | Simular erro fatal (CrashTester), reabrir. | App recupera ou pede login, não entra em loop de crash. |

## 🔹 CATEGORIA B — AUTENTICAÇÃO / PERFIL
| ID | Nome | Ação Humana Simulada | Critério de Sucesso |
|:---|:---|:---|:---|
| **T05** | Login Válido | Digitar credenciais reais lentamente. | Redirecionamento para Dashboard correto. Token salvo. |
| **T06** | Login Inválido | Digitar senha errada. | Shake visual ou mensagem de erro vermelha clara. |
| **T07** | Sessão Expirada | Injetar token vencido no storage. | Auto-logout imediato para tela de login. |
| **T08** | Perfil | Acessar configurações de conta. | Dados do usuário (Nome/Email) visíveis e corretos. |

## 🔹 CATEGORIA C — NAVEGAÇÃO ENTRE TELAS
| ID | Nome | Ação Humana Simulada | Critério de Sucesso |
|:---|:---|:---|:---|
| **T09** | KitchenDashboard | Scroll na lista de pedidos. | Renderização fluida, sem flicker de imagens. |
| **T10** | WaiterDashboard | Alternar entre mesas (Grid). | Status (Livre/Ocupada) atualiza visualmente. |
| **T11** | DriverDashboard | Abrir detalhes da entrega. | Endereço e Mapa visíveis. Botões de ação clicáveis. |
| **T12** | OrdersScreen | Scroll rápido (Fling) em lista grande. | FlashList mantém 60fps. Sem áreas brancas. |
| **T13** | OrderEntry | Adicionar item e observação. | Item aparece no carrinho com a observação correta. |
| **T14** | OrderReview | Remover item do carrinho. | Total atualizado instantaneamente. Botão de envio habilita/desabilita. |

## 🔹 CATEGORIA D — FLUXO CRÍTICO
| ID | Nome | Ação Humana Simulada | Critério de Sucesso |
|:---|:---|:---|:---|
| **T15** | PaymentScreen | Gerar Pix. | QR Code renderiza. Botão de copiar funciona. |
| **T16** | PrinterDebug | Buscar impressora Bluetooth. | Lista de devices não vazia (ou timeout tratado graciosamente). |
| **T17** | WaiterCalls | Simular chamado de mesa. | Toast/Notificação aparece no topo. Som toca. |
| **T18** | Timeout API | Cortar rede durante request de pedido. | Loading infinito prevenido, botão retry aparece. |

## 🔹 CATEGORIA E — QUALIDADE VISUAL
| ID | Nome | Ação Humana Simulada | Critério de Sucesso |
|:---|:---|:---|:---|
| **T19** | Design System | Verificar contraste e fontes. | Sem fontes padrão do sistema (Arial/Roboto cru). Cores do tema. |
| **T20** | Stress Visual | Abrir/Fechar modais 10x rápido. | Sem vazamento de memória ou lag progressivo. |

