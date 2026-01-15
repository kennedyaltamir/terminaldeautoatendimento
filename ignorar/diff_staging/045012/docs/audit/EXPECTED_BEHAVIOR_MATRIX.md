# 🧭 Matriz de Comportamento Esperado do Sistema (L6)
**Status:** SSOT (Single Source of Truth) para Validação de QA
**Versão:** 2.0 — Cobertura Total (38 Páginas)
**Data:** 15/01/2026

Este documento detalha o comportamento esperado para cada interação em todas as telas do ecossistema MesaFlow.

---

## 1. Módulo Público & Cliente (PWA/Landing)

### 1.1. Landing Page (`/`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Botão "Começar Agora" | Clique | Navega para `/admin/register`. |
| Botão "Ver Demo" | Clique | Abre `DemoModal` com opções de segmentos. |
| Seletor de Idioma | Clique | Altera o dicionário de textos (PT/EN/ES) sem recarregar a página. |
| Botão "Login" | Clique | Navega para `/admin/login`. |

### 1.2. Cardápio Digital (`/[slug]/menu`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Card de Produto | Clique | Abre `ProductModal`. Se o produto tiver recomendações, abre `UpsellModal` após fechar o primeiro. |
| Botão "Adicionar" | Clique | Adiciona item ao `CartContext`. Se for a primeira vez, solicita nome do cliente. |
| Botão "Ver Carrinho" | Clique | Abre drawer lateral com resumo do pedido. |
| Botão "Chamar Garçom" | Clique | Abre `ServiceModal`. Envia sinal via WS para o App do Garçom e KDS. |
| Botão "Minha Comanda" | Clique | Abre `ComandaView` listando todos os pedidos da sessão atual da mesa. |
| Parâmetro `?order=ID` | Load | Carrega diretamente a `OrderStatusView` para o pedido específico (Deep Link). |

### 1.3. Kiosk / Totem (`/[slug]/kiosk`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Tela de Atração | Toque | Inicia sessão e navega para o menu em modo totem. |
| Timer de Inatividade | Passivo | Após 60s sem toque, exibe `InactivityModal`. Se não houver resposta em 10s, volta para tela de atração. |

### 1.4. Monitor Público (`/[slug]/monitor`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Lista de Pedidos | Passivo | Atualiza via WS. Pedidos `ready` aparecem em destaque (Verde) com alerta sonoro. |

---

## 2. Módulo Administrativo (Backoffice)

### 2.1. Dashboard (`/admin/[slug]/dashboard`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Filtros (Hoje/7D/Mês) | Clique | Dispara `getDashboardMetrics` e atualiza gráficos do Recharts. |
| Botão "Exportar CSV" | Clique | Gera e baixa arquivo com histórico de vendas do período. |
| Card de KPI | Hover | Exibe tendência percentual em relação ao período anterior. |

### 2.2. Gestão de Cardápio (`/admin/[slug]/menu`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Toggle "Disponível" | Clique | Altera `is_available` no banco. Produto fica opaco no menu do cliente instantaneamente. |
| Botão "Ficha Técnica" | Clique | Abre `RecipeModal` para vincular ingredientes ao produto. |
| Botão "Importar iFood" | Clique | Solicita URL do iFood e popula categorias/produtos automaticamente. |

### 2.3. Gestão de Mesas (`/admin/[slug]/tables`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Botão "Gerar QR Codes" | Clique | Abre visualização de impressão com todos os QRs das mesas ativas. |
| Card de Mesa | Drag | Altera `position_x/y` no banco para salvar o layout do salão. |
| Botão "Fechar Mesa" | Clique | Calcula total + gorjeta, gera Pix (se configurado) e encerra `TableSession`. |

### 2.4. Auditoria Financeira (`/admin/[slug]/audit/financial`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Tabela Ledger | Load | Exibe cadeia de hashes imutável. Se houver quebra de integridade, exibe alerta vermelho. |
| Botão "Fix Orphan" | Clique | Reconcilia transação do gateway que não possui registro no banco local. |

---

## 3. Módulo Operacional (Staff)

### 3.1. KDS / Cozinha (`/admin/[slug]/kitchen`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Card de Pedido | Clique | Avança status: Pendente -> Preparando -> Pronto. |
| Atalhos (1, 2, 3...) | Teclado | Avança o status do pedido na posição correspondente da grade. |
| Botão "Voz" | Clique | Ativa reconhecimento de voz. Comando "Pedido X pronto" avança o status. |

### 3.2. App do Garçom (`/admin/[slug]/waiter`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Botão "Transferir" | Clique | Move todos os pedidos de uma mesa para outra. Se a destino estiver ocupada, oferece "Merge". |
| Botão "Dividir Conta" | Clique | Abre `SplitBillModal`. Permite pagar valor exato, dividir por pessoas ou por itens. |

### 3.3. App do Entregador (`/admin/[slug]/driver`)
| Elemento | Ação | Comportamento Esperado |
| :--- | :--- | :--- |
| Botão "Pegar Pedido" | Clique | Atribui `driver_id` ao pedido e muda status para `delivering`. |
| Botão "Waze/Maps" | Clique | Abre aplicativo externo com coordenadas do endereço de entrega. |
| Botão "Finalizar" | Clique | Solicita código de confirmação (se configurado) e encerra entrega. |

---

## 4. Fluxos Transversais

### 4.1. Segurança & Auth
| Evento | Comportamento Esperado |
| :--- | :--- |
| Login Sucesso | Salva JWT no LocalStorage e redireciona baseado na Role (Kitchen -> KDS, Driver -> DriverApp). |
| Erro 401 (API) | Interceptor dispara `refresh_token`. Se falhar, limpa storage e força redirecionamento para `/login`. |
| Acesso Cross-tenant | O RLS do PostgreSQL bloqueia o retorno de dados, resultando em 404 ou lista vazia, mesmo com token válido. |

### 4.2. Resiliência Offline
| Evento | Comportamento Esperado |
| :--- | :--- |
| Queda de Internet | Exibe `NetworkStatus` (Banner Vermelho). Permite continuar navegando no menu (Cache). |
| Pedido Offline | Salva no `MesaFlowDB` (IndexedDB). Sincroniza automaticamente ao detectar volta da rede. |

---
*Documento gerado pelo Kernel de Governança MesaFlow.*
