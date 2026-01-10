# DOMAIN: PRODUCT / SALES_ENABLEMENT
# TASK_TYPE: KERNEL_INDA
# STATUS: OPEN

🧾 1. IDENTIFICAÇÃO RÍGIDA
TASK_ID: TASK-GTM-08
TITLE: Onboarding "Zero-Touch" & Importador de Cardápio iFood
OWNER: Executor Kernel
PRIORITY: CRÍTICA (SALES VELOCITY)
EXECUTION_MODE: AUTONOMA

🧠 2. ESTADO ATUAL (BASELINE)
## ESTADO_ATUAL
- O cadastro de produtos e categorias é 100% manual via formulários.
- A barreira de entrada para um novo restaurante é alta (tempo gasto cadastrando 50+ itens).
- Não existe um fluxo de "Primeiro Valor" (Aha! Moment) imediato após o registro.
- O sistema está pronto para operar, mas não para escalar vendas self-service.

🎯 3. ESTADO FINAL DESEJADO (OBJETIVO)
## ESTADO_FINAL
- Implementação de um "Wizard" de onboarding no primeiro login.
- Criação de um serviço importador que aceita uma URL pública do iFood e popula automaticamente as categorias e produtos (nome, descrição, preço).
- Redução do tempo de setup inicial de 2 horas para 5 minutos.

🧩 4. ESCOPO FECHADO
## ESCOPO
### INCLUI
- Endpoint `POST /api/admin/menu/import/ifood`.
- Lógica de scraping/parsing de cardápio público iFood.
- UI de progresso de importação no Frontend.
- Automação de criação de 1ª mesa e 1º QR Code no cadastro.

### EXCLUI
- Importação de fotos (devido a direitos autorais e complexidade de storage em massa inicial).
- Sincronização contínua (apenas carga inicial).

✅ 5. CRITÉRIOS DE ACEITAÇÃO (BINÁRIOS)
- [ ] Importador processa URL válida e cria registros no DB.
- [ ] O sistema impede duplicidade de importação.
- [ ] O usuário recebe feedback de sucesso/falha por item.
