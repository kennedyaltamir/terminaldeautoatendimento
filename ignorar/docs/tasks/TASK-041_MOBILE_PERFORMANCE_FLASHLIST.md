# DOMAIN: MOBILE
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-041
TITLE: Otimizar Performance de Renderização de Listas KDS com FlashList
OWNER: Executor Kernel
PRIORITY: ALTA
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- A tela `OrdersScreen` utiliza o componente `FlatList` do React Native padrão.
- Em operações de alto volume (100+ pedidos), a renderização sofre quedas de FPS (frames por segundo) durante o scroll.
- Não há reciclagem avançada de células de memória para listas complexas.
- O projeto já utiliza Expo SDK 54.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- A `OrdersScreen` utiliza `@shopify/flash-list` em substituição ao `FlatList`.
- A propriedade `estimatedItemSize` está configurada corretamente baseada na altura média do card de pedido.
- A performance de scroll mantém 60fps mesmo com 100 itens na lista.
- O componente `FlatList` foi removido das importações da tela de pedidos.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Instalação da dependência `@shopify/flash-list`.
- Refatoração de `mobile/src/screens/orders/OrdersScreen.tsx` para implementar `FlashList`.
- Ajuste de layout (padding/contentContainerStyle) para compatibilidade com FlashList.
- Configuração de `estimatedItemSize` (valor fixo baseado no Design System).

### EXCLUI
- Alterações na lógica de negócio (Store/Service).
- Alterações no design visual dos cards (apenas a lista container muda).
- Otimização de outras listas (apenas KDS Orders neste momento).

🛠️ 5. RESTRIÇÕES TÉCNICAS
## RESTRIÇÕES
- Linguagem: TypeScript.
- Componente: FlashList (Shopify).
- Alterar arquitetura: NÃO.

📥 6. ENTRADAS GARANTIDAS
## ENTRADAS
- Código fonte atual de `OrdersScreen.tsx`.
- Altura estimada do card de pedido (~180px).

📤 7. SAÍDAS ESPERADAS
## SAÍDAS
- `mobile/package.json` atualizado.
- `mobile/src/screens/orders/OrdersScreen.tsx` refatorado.

✅ 8. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
## CRITÉRIOS_DE_ACEITAÇÃO
- [ ] O projeto compila sem erros de dependência.
- [ ] A lista de pedidos renderiza visualmente idêntica à versão anterior.
- [ ] O scroll é fluido.
- [ ] Não há warnings de "FlashList: Missing estimatedItemSize".

🧪 9. PROCEDIMENTO DE VALIDAÇÃO
## VALIDAÇÃO
COMANDO: `npx expo start`
RESULTADO_ESPERADO: App abre, lista carrega, scroll funciona sem engasgos.

🔁 10. ROLLBACK OBRIGATÓRIO
## ROLLBACK
- Reverter `OrdersScreen.tsx` para usar `FlatList`.
- Desinstalar `@shopify/flash-list`.

🔒 11. PROIBIÇÕES EXPLÍCITAS
## PROIBIÇÕES
- É PROIBIDO usar `FlatList` dentro de `ScrollView` (Nested Virtualization).
- É PROIBIDO alterar a lógica de `renderItem` (apenas a props da lista).
