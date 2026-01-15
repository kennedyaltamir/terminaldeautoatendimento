# 🪑 Tela: Gestão de Mesas & QR Codes
**Rota:** `/admin/[slug]/tables`
**Domínio:** ADMIN / MANAGEMENT

## 1. Especificação Visual
- **Canvas de Layout:** Área para posicionar mesas visualmente.
- **Grid de Mesas:** Lista com número da mesa e status (Ativa/Inativa).
- **Preview de QR Code:** Miniatura do código gerado para cada mesa.

## 2. Elementos Interagíveis
- **Botão "Adicionar Mesa":** Cria novo registro e gera token único.
- **Botão "Gerar PDF":** Cria arquivo pronto para impressão com logo e QR.
- **Toggle "Status":** Ativa/Desativa a mesa para pedidos.

## 3. Comportamento Esperado
- **Segurança:** Cada QR Code contém um token criptográfico que impede o cliente de "adivinhar" a URL de outra mesa.
- **Impressão:** O PDF gerado deve seguir o padrão de 10x10cm para displays de mesa.

## 4. APIs Consumidas
- `GET /api/admin/tables`
- `POST /api/admin/tables/bulk`
- `DELETE /api/admin/tables/{id}`

