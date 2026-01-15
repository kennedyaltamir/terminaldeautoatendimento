
# 🧪 Matriz de Testes Human-Like (L5)

**Status:** ATIVO
**Executor:** Maestro + Optimus Kernel
**Objetivo:** Simular comportamento humano para validação visual e funcional.

## 🔹 CATEGORIA A — BOOT / CONTEXTO
| ID | Nome | Ação Humana Simulada | Critério de Sucesso |
|:---|:---|:---|:---|
| **T01** | Cold Start | Abrir app do zero (kill process antes). | Splash some < 2s, Home carrega. |
| **T02** | Hot Reload | Minimizar app e voltar em 5s. | Estado mantido, sem reload branco. |
| **T03** | Offline Boot | Ativar modo avião, abrir app. | Tela de "Sem Conexão" ou Cache visível. |
| **T04** | Crash Recovery | Simular erro fatal, reabrir. | App recupera ou pede login, não crasha loop. |

## 🔹 CATEGORIA B — AUTENTICAÇÃO
| ID | Nome | Ação Humana Simulada | Critério de Sucesso |
|:---|:---|:---|:---|
| **T05** | Login Válido | Digitar credenciais reais lentamente. | Redirecionamento para Dashboard correto. |
| **T06** | Login Inválido | Digitar senha errada. | Shake visual ou mensagem de erro vermelha. |
| **T07** | Sessão Expirada | Injetar token vencido. | Auto-logout para tela de login. |
| **T08** | Perfil | Acessar configurações de conta. | Dados do usuário (Nome/Email) visíveis. |

## 🔹 CATEGORIA C — NAVEGAÇÃO
| ID | Nome | Ação Humana Simulada | Critério de Sucesso |
|:---|:---|:---|:---|
| **T09** | KitchenDashboard | Scroll na lista de pedidos. | Renderização fluida, sem flicker. |
| **T10** | WaiterDashboard | Alternar entre mesas. | Status (Livre/Ocupada) atualiza. |
| **T11** | DriverDashboard | Abrir detalhes da entrega. | Endereço e Mapa visíveis. |
| **T12** | OrdersScreen | Scroll rápido (Fling). | FlashList mantém 60fps. |
| **T13** | OrderEntry | Adicionar item e obs. | Item aparece no carrinho. |
| **T14** | OrderReview | Remover item do carrinho. | Total atualizado instantaneamente. |

## 🔹 CATEGORIA D — FLUXO CRÍTICO
| ID | Nome | Ação Humana Simulada | Critério de Sucesso |
|:---|:---|:---|:---|
| **T15** | PaymentScreen | Gerar Pix. | QR Code renderiza. |
| **T16** | PrinterDebug | Buscar impressora. | Lista de devices não vazia (ou timeout tratado). |
| **T17** | WaiterCalls | Simular chamado. | Toast/Notificação aparece. |
| **T18** | Timeout API | Cortar rede durante request. | Loading infinito prevenido, botão retry. |

## 🔹 CATEGORIA E — QUALIDADE VISUAL
| ID | Nome | Ação Humana Simulada | Critério de Sucesso |
|:---|:---|:---|:---|
| **T19** | Design System | Verificar contraste e fontes. | Sem fontes padrão do sistema (Arial/Roboto cru). |
| **T20** | Stress Visual | Abrir/Fechar modais 10x. | Sem vazamento de memória ou lag. |

