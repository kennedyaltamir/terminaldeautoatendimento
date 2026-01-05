# 👨‍🍳 Detalhamento Técnico: KDS Pro Features (KDS-03)

## 1. Problema Atual
O KDS atual trata todos os pedidos com a mesma prioridade visual. Cozinhas complexas precisam identificar gargalos de tempo e separar o que é "Para Viagem" do que é "Mesa" de forma agressiva.

## 2. Solução Proposta
Implementar inteligência de fluxo e alertas sensoriais na cozinha.

### 2.1 Funcionalidades Avançadas
- **SLA Visual Dinâmico:** O card muda de cor gradualmente (Verde -> Amarelo -> Vermelho) baseado no tempo médio de preparo configurado para cada categoria.
- **Agrupador de Itens:** Uma aba lateral que soma todos os itens iguais pendentes (ex: "Preparar 12 Hambúrgueres no total") para otimizar a chapa.
- **Recall Inteligente:** Botão para desfazer a finalização de um pedido nos últimos 60 segundos.
- **Alerta Sonoro Diferenciado:** Sons distintos para Pedido Novo, Pedido Atrasado e Chamado de Garçom.

## 3. Arquivos a Alterar/Criar
- `frontend/src/components/admin/KDS/ItemAggregator.tsx`: Novo componente de resumo de produção.
- `frontend/src/components/admin/KDS/OrderCard.tsx`: Lógica de cores baseada em timers.
- `app/models.py`: Adicionar `target_prep_time` no modelo de Categoria.

## 4. Testes
- Validar se o contador de tempo não reinicia ao atualizar a página (persistência de `created_at`).
- Testar a performance do WebSocket com 100+ pedidos ativos simultâneos.
