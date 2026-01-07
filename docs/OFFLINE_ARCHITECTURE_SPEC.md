# 📡 Especificação da Arquitetura Offline-First

## 1. Camada de Persistência Local
Utilizamos o **Dexie.js** como wrapper sobre o IndexedDB do navegador. O banco local é chamado `MesaFlowDB`.

### Tabelas Locais
- `pendingOrders`: Armazena pedidos realizados pelo garçom em áreas de sombra de Wi-Fi.
- `fiscalQueue`: Armazena solicitações de emissão de NFC-e feitas em modo offline.

## 2. Motor de Sincronização (Sync Engine)
A sincronização não é baseada em intervalos fixos, mas em **eventos de conectividade**.

### Fluxo de Trabalho:
1.  **Captura:** O usuário realiza a ação (ex: Emitir Nota).
2.  **Detecção:** O sistema checa `navigator.onLine`.
3.  **Store:** Se offline, salva no Dexie com `status: 'pending'`.
4.  **Forward:** Ao detectar o evento `window.online`, o hook `useFiscalSync` ou `useOfflineSync` percorre a tabela e envia os dados via POST.
5.  **Cleanup:** Após o sucesso (200 OK), o item é removido do banco local para liberar espaço.

## 3. Resiliência e Retries
- **Erros 4xx:** Se o servidor rejeitar o dado (erro de validação), o item é marcado como `status: 'error'` e a sincronização para aquele item é suspensa até intervenção manual.
- **Erros 5xx/Timeout:** O sistema incrementa o `retryCount` e tenta novamente na próxima janela de conexão.

---
# 📡 Especificação Técnica: Modo Offline-First

## 1. Persistência com Dexie.js
O frontend não confia na rede para operações críticas. Utilizamos o IndexedDB para garantir que nenhum dado seja perdido.

### Estrutura da Fila (`fiscalQueue`)
| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | Auto-increment | Chave local |
| `orderId` | UUID | Referência do pedido no backend |
| `status` | String | `pending` ou `error` |
| `retryCount` | Integer | Tentativas de envio |

## 2. Ciclo de Sincronização
O hook `useFiscalSync` opera em três gatilhos:
1.  **Evento `online`:** Disparado pelo browser quando a rede volta.
2.  **Montagem do Componente:** Verifica a fila ao abrir a página de histórico.
3.  **Intervalo de Segurança:** A cada 60s, tenta reenviar itens com `status: 'pending'`.

## 3. Idempotência no Backend
O backend utiliza o `order_id` como chave de trava. Se o frontend enviar a mesma nota duas vezes devido a uma oscilação de rede, o backend detecta que o `fiscal_status` já é `emitted` ou `processing` e ignora a segunda requisição, retornando a URL da nota já existente.

---
