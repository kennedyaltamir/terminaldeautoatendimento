# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 08:35:00
# 🖥️ AdminSettingsPage
> **Plataforma:** Web (Next.js 14)
> **Rota:** `/admin/[slug]/settings`
> **Acesso:** Protected (Owner)
> **Status:** VALIDATED

## 1. Visão Geral
**Propósito:** Central de configuração do estabelecimento. Permite alterar dados cadastrais, aparência (cores/logo) e horários de funcionamento.
**Persona Principal:** Dono.

## 2. Estrutura de Interface
- **Layout Pai:** `AdminLayout`.
- **Componentes Chave:**
  - `SettingsForm`: Formulário principal com abas (Geral, Aparência, Horários).
  - `ImageUpload`: Componente para Logo e Banner.
  - `ColorPicker`: Seleção de cores da marca.

## 3. Elementos Interativos & Ações
| Elemento | Tipo | Ação | Feedback Visual | Side Effect |
| :--- | :--- | :--- | :--- | :--- |
| `Salvar Alterações` | Button | `handleSubmit` | Spinner + Toast | `PATCH /api/company/me` |
| `Upload Logo` | Input File | `handleUpload` | Preview Imagem | Upload S3 |
| `Cor Primária` | Input Color | `setColor` | Preview em tempo real | State Local |

## 4. Estados da Tela
- **Loading:** Skeleton do formulário.
- **Success:** Toast "Configurações salvas com sucesso".
- **Error:** Toast com mensagem de validação (Zod).

## 5. Fluxos de Navegação
1. **Entrada:** Menu Lateral -> Configurações.
2. **Saída:** Permanência na tela após salvar.

## 6. Regras de Negócio Críticas
- [x] Apenas usuários com role `owner` podem acessar.
- [x] Validação de formato de cor (Hex).
- [x] Upload de imagens limitado a 2MB.

## 7. Dados & Integração
- **API Endpoints:**
  - `GET /api/admin/company/me`
  - `PATCH /api/admin/company/me`
  - `POST /api/upload`

