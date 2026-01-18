# 🧪 AdminSettingsFeaturesPage
> **Plataforma:** WEB | **Domínio:** GOVERNANÇA | **Status:** VALIDATED (Gold Master)

## 1. Propósito e Objetivo
Painel de controle de funcionalidades experimentais (Feature Flags). Destinado à equipe de suporte e desenvolvedores (Modo Impersonation), permite ativar ou desativar módulos Beta para clientes específicos sem a necessidade de novo deploy de código.

## 2. Estrutura e Layout
- **Feature List:** Grid de cards contendo o nome técnico da flag, descrição funcional e status atual.
- **Support Banner:** Aviso persistente de que o "Modo Suporte" está ativo e as alterações são auditadas.

## 3. Elementos Interativos
- **Feature Toggle:** Switch para ligar/desligar funcionalidades em tempo real.
- **Audit Link:** Atalho para visualizar quem alterou a flag e quando.

## 4. Regras de Segurança (L6)
- **Impersonation Only:** Esta página é invisível e inacessível para lojistas comuns. Exige a claim `impersonator: true` no JWT.
- **Optimistic Rollback:** Se a API falhar ao salvar a flag, a UI reverte o toggle automaticamente para o estado anterior.
- **Cache Invalidation:** A alteração limpa o cache de flags do Tenant no Redis instantaneamente.

## 5. Estados da Tela
- **Loading:** Busca das flags ativas para o Tenant selecionado.
- **Unauthorized:** Bloqueio total com log de tentativa de acesso indevido.
- **Success Toast:** Confirmação de que a funcionalidade foi propagada para o ambiente do cliente.

## 6. Fluxo de Dados (API)
- **Fetch:** `GET /api/admin/features`
- **Update:** `POST /api/admin/features` (Payload: `{ key: string, is_enabled: bool }`)

---
![Features Preview](https://raw.githubusercontent.com/mesaflow/assets/main/screenshots/admin-features.png)

