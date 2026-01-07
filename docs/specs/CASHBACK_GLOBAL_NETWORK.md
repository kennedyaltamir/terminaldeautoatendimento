# 🌐 MesaFlow Passport: Rede Global de Cashback e Indicações

## 1. Visão Geral
O **MesaFlow Passport** é o módulo B2B2C que unifica a experiência do cliente final em toda a rede de estabelecimentos que utilizam o ecossistema MesaFlow. O objetivo é criar um efeito de rede onde o cashback acumulado em um local possa ser resgatado em qualquer outro parceiro da plataforma.

## 2. O Conceito "MesaFlow ID"
Em vez de múltiplos cadastros, o cliente possui uma identidade única baseada no seu número de telefone.
- **Login Simplificado:** Sem senhas complexas. Acesso via link mágico ou código via WhatsApp.
- **Carteira Unificada:** O saldo de cashback é um ativo global do usuário dentro da rede MesaFlow.

## 3. Fluxo de Funcionamento

### 3.1. Acúmulo (Earning)
1. O cliente realiza um pedido em qualquer estabelecimento da rede.
2. Ao informar o telefone no checkout, o sistema calcula o cashback baseado na regra daquela loja (ex: 5%).
3. O saldo é creditado na conta global do usuário.

### 3.2. Resgate (Redemption)
1. O cliente visita um novo estabelecimento da rede.
2. O sistema identifica o saldo disponível via telefone.
3. O cliente pode optar por abater o valor da conta.
4. **Regra de Compensação:** O valor resgatado é descontado da fatura mensal que o estabelecimento paga ao MesaFlow, ou processado via fundo de reserva da plataforma.

### 3.3. Área do Embaixador (Referral)
O cliente logado tem acesso a um dashboard exclusivo:
- **Extrato Global:** Onde ele ganhou e onde gastou.
- **Mapa da Rede:** Onde ele pode gastar o saldo dele (Geolocalização de parceiros).
- **Indique e Ganhe:** Link personalizado para indicar o MesaFlow a novos donos de estabelecimentos.
    - **Recompensa:** Se o indicado assinar o plano PRO, o embaixador ganha R$ 50,00 em cashback global imediato.

## 4. Impacto no Modelo de Negócio (SaaS -> Platform)
- **Retenção de Estabelecimentos:** O dono do restaurante não cancela o MesaFlow porque ele faz parte de uma rede que traz clientes com saldo para gastar.
- **Aquisição de Clientes (CAC Zero):** Os próprios usuários finais vendem o sistema para novos estabelecimentos para expandir suas opções de uso do cashback.
- **Big Data:** Visão 360º do hábito de consumo do cliente (ele gosta de pizza na sexta, mas frequenta hotéis aos finais de semana).

## 5. Requisitos Técnicos para Implementação
- **Banco de Dados:** Criar esquema `global` separado dos esquemas de `tenant`.
- **Segurança:** Implementar JWT com escopo `client_user` diferente de `admin_user`.
- **API:** Novos endpoints:
    - `GET /passport/balance`: Consulta de saldo global.
    - `POST /passport/referral`: Registro de indicação.
    - `GET /passport/partners`: Lista de locais que aceitam o Passport.

---
*Documento de Especificação v1.0 - Janeiro 2026*
# 🌐 MesaFlow Passport: Especificação da Rede Global

## 1. Arquitetura de Identidade (MesaFlow ID)
O usuário não pertence mais a uma "Loja", mas à "Plataforma".
- **Chave Única:** Número de Telefone (E.164).
- **Autenticação:** Passwordless (Link Mágico ou WhatsApp OTP).
- **Perfil:** Nome, E-mail, Preferências Alimentares e Histórico de Consumo Transversal.

## 2. Economia do Cashback Global
### 2.1. Fluxo de Crédito
- O lojista define sua taxa (ex: 5%).
- O valor é calculado sobre o `total_amount` pago.
- O crédito entra na `GlobalWallet` do usuário com a tag da loja de origem.

### 2.2. Fluxo de Débito (O Pulo do Gato)
- O usuário decide usar R$ 10,00 de saldo no Restaurante B.
- O Restaurante B recebe o valor total da venda (R$ 10,00 vêm do saldo MesaFlow).
- **Compensação:** O MesaFlow debita R$ 10,00 do saldo devedor do Restaurante B na fatura do SaaS ou realiza um "netting" (encontro de contas) entre os lojistas da rede.

## 3. Portal do Embaixador (Growth Hacking)
Interface exclusiva para o cliente final (`app.mesaflow.com/passport`):

### 3.1. Funcionalidades
- **Saldo Unificado:** Visualização clara de quanto ele tem para gastar na rede.
- **Onde Gastar:** Mapa interativo (Google Maps API) mostrando estabelecimentos MesaFlow próximos.
- **Módulo de Indicação (Referral):**
    - Botão "Indicar este Restaurante".
    - Link único: `mesaflow.com/register?ref=USER_ID`.
    - **Gamificação:** Ranking de embaixadores com badges (Bronze, Prata, Gold).

### 3.2. Recompensas de Indicação
- **Lead Qualificado:** Se o restaurante indicado criar uma conta, o embaixador ganha um badge.
- **Conversão (Assinatura):** Se o restaurante assinar o plano PRO, o embaixador recebe um crédito fixo (ex: R$ 50,00) para gastar em qualquer lugar da rede.

## 4. Estrutura de Dados (Novas Tabelas)
- `global_users`: id, phone, name, email, referral_code.
- `global_wallets`: user_id, balance, total_earned, total_spent.
- `global_transactions`: id, user_id, company_id (origem/destino), amount, type (earn/spend/referral).
- `referrals`: id, ambassador_id, referred_company_id, status (pending/converted), reward_paid.

## 5. Roadmap de Implementação
1. **Sprint 1:** Centralização da tabela de carteiras e criação do endpoint de saldo global.
2. **Sprint 2:** Implementação do login via WhatsApp OTP.
3. **Sprint 3:** Lançamento da interface "Área do Cliente" com extrato.
4. **Sprint 4:** Lançamento do sistema de links de indicação.
