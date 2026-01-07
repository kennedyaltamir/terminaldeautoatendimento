# 💾 Estratégia de Dados e Concorrência

## 1. Modelo de Concorrência
O MesaFlow é um sistema multi-dispositivo. A política oficial de resolução de conflitos é:
**Server-Wins com controle de versão (Optimistic Locking).**

- **Proposta vs Confirmação:** O aplicativo apenas propõe alterações ao estado dos dados. O "último write" válido é sempre aquele aceito e confirmado pelo servidor.
- **Resolução:** O App nunca tenta resolver conflitos de dados complexos localmente; em caso de rejeição pelo servidor, o estado local deve ser invalidado e sincronizado com a verdade do banco de dados.
- **Sincronia:** WebSockets garantem que se um garçom alterar um pedido no App, a tela do KDS na Web atualize em < 100ms.

## 2. Cache e Offline
- **React Query:** Cache em memória para navegação instantânea.
- **AsyncStorage:** Persistência de dados não sensíveis (preferências, rascunhos de pedidos).
- **Fila de Sincronização:** Pedidos feitos offline são enfileirados e disparados assim que a conectividade for detectada.

## 3. Segurança
- **SSL Pinning:** (Futuro) Para evitar ataques Man-in-the-Middle em redes Wi-Fi públicas.
- **Data Masking:** Informações sensíveis de clientes (CPF/Cartão) nunca são armazenadas localmente.
