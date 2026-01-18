# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 08:35:00
# 🖥️ AdminFeaturesPage
> **Plataforma:** Web (Next.js 14)
> **Rota:** `/admin/[slug]/settings/features`
> **Acesso:** Protected (Support/God Mode)
> **Status:** VALIDATED

## 1. Visão Geral
**Propósito:** Controle de Feature Flags (Canary Releases). Permite ativar/desativar módulos experimentais por tenant.
**Persona Principal:** Suporte Técnico, Desenvolvedor.

## 2. Estrutura de Interface
- **Layout Pai:** `AdminLayout`.
- **Componentes Chave:**
  - `FeatureToggleCard`: Card com descrição da feature e switch on/off.
  - `SupportModeBanner`: Aviso visual de que o usuário está em modo de suporte.

## 3. Elementos Interativos & Ações
| Elemento | Tipo | Ação | Feedback Visual | Side Effect |
| :--- | :--- | :--- | :--- | :--- |
| `Toggle` | Switch | `handleToggle` | Optimistic UI | `POST /api/features` |

## 4. Estados da Tela
- **Read-Only:** Para usuários normais (Owner), mostra as features mas não permite editar.
- **Edit:** Para usuários com claim `impersonator: true`.

## 5. Fluxos de Navegação
1. **Entrada:** Configurações -> Funcionalidades Beta.

## 6. Regras de Negócio Críticas
- [x] Edição restrita a tokens de suporte.
- [x] Rollback automático da UI em caso de erro na API.

## 7. Dados & Integração
- **API Endpoints:**
  - `GET /api/admin/features`
  - `POST /api/admin/features`

