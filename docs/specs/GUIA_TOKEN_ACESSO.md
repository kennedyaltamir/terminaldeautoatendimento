# 🔑 Guia do Token de Acesso (PIN de Mesa)

O **Token de Acesso** é um código de segurança de 10 dígitos gerado automaticamente pelo MesaFlow sempre que uma mesa é aberta. Ele serve como a "chave mestra" para que o cliente ou o staff recupere uma sessão de pedido ativa.

---

## 1. Para que serve?
*   **Recuperação de Conexão:** Se o cliente fechar o navegador por engano ou a bateria do celular acabar, ele pode usar o Token em outro aparelho para continuar o pedido de onde parou.
*   **Segurança:** Garante que apenas pessoas autorizadas (quem está na mesa ou o staff) possam adicionar itens à comanda.
*   **Suporte do Garçom:** Permite que o garçom valide a identidade do cliente antes de realizar transferências ou fechamentos.

---

## 2. Onde encontrar o Token?

### A. No App do Garçom (Lista de Mesas)
Na tela principal do garçom (`/waiter`), o token aparece em todos os cards de mesas **ocupadas**.
*   **Localização:** Logo abaixo do nome do cliente.
*   **Visual:** Uma etiqueta azul com o ícone de chave 🔑.
*   **Exemplo:** `Token: 1554989519`

### B. No App do Garçom (Dentro da Mesa)
Ao clicar em uma mesa para lançar produtos, o token fica fixo no topo.
*   **Localização:** No cabeçalho (Header), abaixo do número da mesa.
*   **Visual:** Texto em destaque: `TOKEN: XXXXXXXXXX`.

### C. No Painel Administrativo (Gestor)
Na aba **Mesas**, ao clicar em uma mesa que está com o status "Ocupada".
*   **Localização:** Dentro do modal de detalhes da mesa.
*   **Visual:** Um bloco escuro centralizado com o título **TOKEN DE ACESSO**.

---

## 3. Como ajudar o cliente?

Se o cliente visualizar a tela de **"Mesa Ocupada"** no celular dele:

1.  O garçom localiza o código de 10 dígitos no seu próprio celular.
2.  O garçom dita os números para o cliente.
3.  O cliente clica em **"Tenho o Token de Acesso"** no celular dele.
4.  O cliente digita o código e clica na seta para entrar.
5.  **Pronto!** A comanda é restaurada instantaneamente.

---

## ⚠️ Notas de Segurança
*   **Troca de Token:** O token é único por sessão. Quando a mesa é fechada e aberta novamente para outro cliente, um novo código de 10 dígitos é gerado.
*   **Privacidade:** O garçom nunca deve ditar o token de uma mesa para clientes de outra mesa.
*   **Perda Total:** Caso o token seja perdido e não apareça na tela (erro raro), o gerente pode fechar a mesa manualmente pelo painel e abrir uma nova.

---
*Documentação atualizada para MesaFlow v2.3 - Janeiro 2026*
