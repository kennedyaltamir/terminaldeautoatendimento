# 🚀 MesaFlow: O Sistema Operacional para Ambientes de Alto Tráfego

> **Slogan:** Transforme mesas em pontos de venda inteligentes e elimine a fricção entre o cliente e a cozinha.

## 📝 Resumo do Projeto
O **MesaFlow** é uma plataforma SaaS (*Software as a Service*) Fullstack desenvolvida para modernizar a operação de food service de ponta a ponta. Mais do que um cardápio digital, ele é um ecossistema que centraliza a operação em uma única nuvem, conectando o salão, a cozinha, o delivery e o back-office em tempo real.

O grande diferencial do MesaFlow é sua **Arquitetura Híbrida**: ele permite que o autoatendimento (via QR Code) e o atendimento tradicional (via Garçom) coexistam na mesma comanda, garantindo agilidade sem perder a hospitalidade.

---

## ⚙️ Como Funciona (Pilares da Solução)

### 1. Experiência do Cliente (Autoatendimento Sem Atrito)
O sistema transforma cada mesa em um PDV autônomo.
*   **Zero App:** O cliente escaneia um QR Code e acessa um cardápio digital interativo instantaneamente, sem precisar baixar nada.
*   **Autonomia Total:** O cliente escolhe, personaliza o pedido e realiza o pagamento (Pix/Cartão) direto pelo celular.
*   **Status em Tempo Real:** O cliente acompanha o progresso ("Preparando", "Pronto") pelo próprio dispositivo, reduzindo a ansiedade e a demanda sobre a equipe.

### 2. Operação Inteligente (KDS & Staff)
Substituímos as impressoras de papel e os gritos na cozinha por tecnologia sincronizada via WebSockets.
*   **KDS (Kitchen Display System):** Telas interativas na cozinha e no bar recebem os pedidos instantaneamente. O sistema organiza a fila de produção, controla o tempo de preparo (SLA) com alertas visuais e separa itens por praça (ex: Bebidas vão para o Bar, Comida para a Cozinha).
*   **App do Garçom:** A equipe de salão possui uma interface móvel poderosa. O garçom pode lançar pedidos na mesma comanda que o cliente abriu, fechar contas e receber chamados, focando na experiência e não apenas na anotação.
*   **Logística de Delivery:** Um módulo dedicado para gerenciar pedidos externos e despachar para entregadores, com rastreamento integrado.

### 3. Gestão 360º (Back-office)
O painel administrativo oferece controle total ao proprietário.
*   **Controle de Acesso (RBAC):** Interfaces e permissões distintas para cada função: Dono, Gerente, Garçom, Cozinheiro e Entregador.
*   **Estoque Inteligente:** Baixa automática de ingredientes baseada na ficha técnica dos produtos vendidos.
*   **Marketing & White Label:** O cardápio permite personalização visual (cores e logo da marca) e gera links públicos para divulgação em redes sociais.

---

## 🌍 Versatilidade Multi-Segmento (A Grande Sacada)
A arquitetura do MesaFlow foi projetada com **escalabilidade vertical**. O sistema abstrai o conceito de "Mesa" para "Ponto de Venda Localizado". Isso permite que a mesma tecnologia seja aplicada em diversos cenários com apenas uma mudança de configuração:

*   🍽️ **Restaurantes:** Gestão de Mesas e Comandas.
*   🏨 **Hotéis:** *Room Service* digital (o QR Code fica no quarto).
*   🏟️ **Estádios e Eventos:** Venda direta no assento/cadeira para evitar filas no intervalo.
*   🏢 **Corporativo:** Gestão de *Coffee Breaks* e praças de alimentação internas.

---

## 🛠️ Destaques Técnicos
*   **Sincronização Real-Time:** Uso de WebSockets para que a cozinha receba o pedido milissegundos após o cliente confirmar.
*   **Alta Disponibilidade:** Preparado para picos de acesso (como o intervalo de um jogo ou almoço executivo).
*   **Integração Financeira:** Split de pagamento automático e gestão de assinaturas.

# 🚀 MesaFlow: O Sistema Operacional para Food Service

O **MesaFlow** é uma plataforma SaaS B2B de missão crítica, desenhada para orquestrar operações em ambientes de alto tráfego (Restaurantes, Hotéis, Estádios e Eventos).

## 🎯 Proposta de Valor
Eliminar a fricção entre o cliente e a cozinha através de uma **Arquitetura Híbrida**:
1.  **Autoatendimento:** Cliente pede e paga via QR Code (PWA), sem baixar apps.
2.  **Operação Assistida:** Staff utiliza um Mobile POS (App do Garçom) sincronizado em tempo real.

## 🛠️ Diferenciais Técnicos
- **Real-time:** WebSockets sobre Redis Pub/Sub para latência sub-100ms.
- **Offline-First:** Sincronização via Dexie.js garante que a operação não pare se o Wi-Fi oscilar.
- **Fintech Embutida:** Split de pagamento automático (Marketplace) e gestão de assinaturas Stripe.
- **Enterprise Ready:** Auditoria de logs, emissão fiscal NFC-e, gestão de franquias e motor de NPS.

## 🔐 Segurança
- Isolamento Multi-tenant via `company_id` (RLS).
- Proteção contra IDOR, XSS e SQL Injection.
- Rate Limiting por IP e Tenant.
