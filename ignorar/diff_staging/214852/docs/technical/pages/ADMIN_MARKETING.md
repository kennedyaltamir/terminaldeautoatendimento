# 📣 Tela: Marketing & Fidelidade
**Rota:** `/admin/[slug]/marketing`
**Domínio:** ADMIN / GROWTH

## 1. Especificação Visual
- **Dashboard de Fidelidade:** Gráfico de retenção e total de cashback distribuído.
- **Lista de Promoções:** Cards com status da campanha (Ativa/Pausada).

## 2. Elementos Interagíveis
- **Configuração de Cashback:** Input para definir a % de retorno por compra (ex: 5%).
- **Criador de Cupons:** Modal para definir código, valor de desconto e validade.
- **Botão "Gerar Recomendações":** Dispara o motor de IA para sugerir upsells baseados no histórico.

## 3. Comportamento Esperado
- **Validação de Cupom:** O sistema impede a criação de códigos duplicados para a mesma empresa.
- **IA Trigger:** O processamento de recomendações é assíncrono e notifica o usuário via Toast quando concluído.

## 4. APIs Consumidas
- `GET /api/admin/marketing/promotions`: Lista de cupons.
- `POST /api/admin/marketing/recommendations/generate`: Trigger do motor de IA.
- `PATCH /api/admin/company/me`: Atualização da regra de cashback.
