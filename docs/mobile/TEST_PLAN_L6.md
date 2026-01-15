
# 🧪 Plano de Testes L6: MesaFlow Mobile (Autonomous Governance)
**Status:** ATIVO
**Executor:** Optimus Kernel
**Meta:** Zero Regressão em Produção

Este plano define os 20 cenários de teste obrigatórios para certificação de loja e estabilidade operacional.

---

## 🔐 BLOCO A — BOOT & LOGIN (Crítico)
| ID | Cenário | Ação do Robô | Critério de Sucesso |
|:---|:---|:---|:---|
| **T01** | Cold Start | Abrir app do zero. | Splash screen -> Login visível em < 2s. |
| **T02** | Warm Start | Minimizar e restaurar. | Estado da tela preservado. |
| **T03** | UI Integrity | Verificar labels e ícones. | "E-mail", "Senha", Logo presentes. |
| **T04** | Login Inválido (E-mail) | Digitar e-mail sem @. | Mensagem de erro inline. |
| **T05** | Login Inválido (Senha) | Digitar senha incorreta. | Mensagem "Credenciais inválidas". |
| **T06** | Login via Teclado | Pressionar ENTER no teclado. | Disparar submit e mostrar erro/sucesso. |

## 🧭 BLOCO B — NAVEGAÇÃO (Core)
| ID | Cenário | Ação do Robô | Critério de Sucesso |
|:---|:---|:---|:---|
| **T07** | Home Load | Login com sucesso. | Dashboard carrega sem skeleton infinito. |
| **T08** | Tab Navigation | Alternar entre abas. | Troca de tela suave (< 100ms). |
| **T09** | API Loading | Simular delay de rede. | Spinner visível durante fetch. |
| **T10** | Offline Mode | Ativar modo avião. | Banner "Sem Conexão" visível. |
| **T11** | Infinite Scroll | Rolar lista de pedidos. | Novos itens carregam sem crash. |

## 🧾 BLOCO C — OPERAÇÃO (Funcional)
| ID | Cenário | Ação do Robô | Critério de Sucesso |
|:---|:---|:---|:---|
| **T12** | Criar Pedido | Fluxo completo de adição. | Pedido aparece na lista local. |
| **T13** | Editar Pedido | Alterar observação. | Mudança reflete na UI. |
| **T14** | Cancelar Pedido | Tentar deletar item. | Modal de confirmação aparece. |
| **T15** | Empty State | Limpar lista. | Ilustração de "Nada por aqui" visível. |

## ⚠️ BLOCO D — RESILIÊNCIA (SRE)
| ID | Cenário | Ação do Robô | Critério de Sucesso |
|:---|:---|:---|:---|
| **T16** | Crash Recovery | Forçar erro JS. | Error Boundary captura e permite retry. |
| **T17** | API Timeout | Simular timeout 30s. | Toast de "Erro de conexão" amigável. |
| **T18** | Background Kill | Matar app em background. | Reabrir exige login ou hidrata token. |

## 🏁 BLOCO E — STORE READINESS
| ID | Cenário | Ação do Robô | Critério de Sucesso |
|:---|:---|:---|:---|
| **T19** | Acessibilidade | Verificar contrastes. | WCAG AA compliant (Cores/Fontes). |
| **T20** | Screenshots | Capturar telas finais. | Imagens limpas para lojas (sem dados de teste). |

---
*Gerado automaticamente pelo Kernel L6.*

