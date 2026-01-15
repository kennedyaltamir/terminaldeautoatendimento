# 🏢 Tela: Gestão de Franquias
**Rota:** `/admin/[slug]/franchise`
**Domínio:** ADMIN / ENTERPRISE

## 1. Especificação Visual
- **Mapa de Unidades:** Lista de lojas vinculadas ao mesmo dono.
- **KPIs Consolidados:** Faturamento global, Loja destaque, CMV médio da rede.
- **Gráfico Comparativo:** Performance de vendas entre unidades.

## 2. Elementos Interagíveis
- **Botão "Acessar Unidade":** Dispara o fluxo de `Impersonation` para gerenciar a filial.
- **Filtro de Rede:** Selecionar grupos de lojas por região.

## 3. Comportamento Esperado
- **Segurança:** Apenas o `owner` master tem acesso a esta visão.
- **Sincronia:** Dados são agregados em tempo real, mas com cache de 5 min para performance.

## 4. APIs Consumidas
- `GET /api/admin/franchise/dashboard`: Dados agregados da rede.
