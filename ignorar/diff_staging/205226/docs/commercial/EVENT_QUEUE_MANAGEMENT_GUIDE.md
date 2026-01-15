# 🎟️ Guia de Gestão de Filas para Grandes Eventos
**MesaFlow OS — Whitepaper Operacional**

## 1. Introdução
Em eventos de massa (estádios, festivais, arenas), o tempo é o recurso mais escasso. Este guia detalha como utilizar o MesaFlow para maximizar o faturamento nos picos de demanda.

## 2. Arquitetura de Fluxo
### 2.1 O Conceito de "Grab & Go"
O cliente realiza o pedido via QR Code no assento. O sistema direciona o pedido para a ilha de produção (KDS) mais próxima. O cliente só se desloca ao balcão quando recebe a notificação "Pronto para Retirada".

### 2.2 Setorização de Produção
- **Ilhas de Bebidas:** KDS configurado apenas para itens de bar.
- **Ilhas de Alimentos:** KDS focado em cozinha quente.
- **Vendedores Móveis:** Staff com App POS realizando vendas na fila física para reduzir a percepção de espera.

## 3. Configurações Críticas no MesaFlow
1.  **Regra 86 (Estoque):** Deve estar ativa para evitar venda de produtos esgotados durante o evento.
2.  **SLA de Alerta:** Configurar para 5 minutos. Se um pedido não for aceito em 5 min, o gerente recebe um alerta crítico.
3.  **Pagamento Pix Automático:** Reduz o tempo de transação de 45s (maquininha) para 5s (confirmação via webhook).

## 4. Checklist para o Dia do Evento
- [ ] Testar cobertura Wi-Fi/4G em todos os setores.
- [ ] Validar sincronia dos WebSockets em 50+ dispositivos simultâneos.
- [ ] Garantir que as impressoras de etiquetas de produção tenham bobinas reserva.
