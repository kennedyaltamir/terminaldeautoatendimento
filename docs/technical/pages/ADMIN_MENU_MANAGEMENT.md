# 🍔 Tela: Gestão de Cardápio
**Rota:** `/admin/[slug]/menu`
**Domínio:** ADMIN / MANAGEMENT

## 1. Especificação Visual
- **Lista de Categorias:** Acordeões expansíveis.
- **Cards de Produto:** Miniatura da imagem, preço, status (Disponível/Pausado).
- **Modais:** Formulário de criação/edição de produto e grupos de opcionais.

## 2. Elementos Interagíveis
- **Switch "Disponibilidade":** Altera `is_available` via PATCH imediato.
- **Botão "Importar iFood":** Abre modal para colar URL do cardápio externo.
- **Drag & Drop:** Reordenação de categorias e produtos (order_index).

## 3. Comportamento Esperado
- **Cache Invalidation:** Ao salvar qualquer alteração, disparar `CacheService.invalidate_menu(slug)` no backend.
- **Upload de Imagem:** Processamento via `S3` ou `Local` com preview instantâneo.
- **Validação:** Impedir preços negativos ou nomes vazios (Zod Schema).

## 4. APIs Consumidas
- `GET /api/admin/menu/products`: Lista completa.
- `POST /api/admin/menu/categories`: Nova categoria.
- `PATCH /api/admin/menu/products/{id}`: Atualização parcial.
- `POST /api/admin/menu/import/ifood`: Crawler de importação.
