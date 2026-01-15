# 🚩 Tela: Funcionalidades Beta (Feature Flags)
**Rota:** `/admin/[slug]/settings/features`
**Domínio:** ADMIN / SUPPORT

## 1. Especificação Visual
- **Lista de Flags:** Cards com Nome da Feature, Descrição Técnica e Switch (On/Off).
- **Banner de Alerta:** Aviso de que alterações podem causar instabilidade.

## 2. Elementos Interagíveis
- **Switch Toggle:** Ativa/Desativa a flag no banco de dados.
- **Botão "Limpar Cache":** Força a atualização do Redis para que a flag seja aplicada imediatamente.

## 3. Comportamento Esperado
- **Restrição:** Esta página é invisível para o cliente. Só aparece se o token JWT contiver a claim `impersonator: true`.
- **Audit Log:** Toda alteração de flag gera um log de auditoria obrigatório.

## 4. APIs Consumidas
- `GET /api/admin/features`: Lista de flags do Tenant.
- `POST /api/admin/features`: Atualização de estado.

