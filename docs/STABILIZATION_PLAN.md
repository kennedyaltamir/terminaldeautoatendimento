# 🛡️ Plano de Estabilização e Anti-Retrabalho (Omni-Check)
**Status:** ESTRATÉGICO
**Objetivo:** Impedir que novas funcionalidades quebrem o legado.

## 1. O Conceito Omni-Check
Fica estabelecido que nenhum código será considerado "Done" sem passar pelo **MesaFlow Omni-Check**.
Este é um script mestre (`scripts/validation/omni_check.py`) que dispara simultaneamente:
1.  **Integridade de Dados:** Valida se as tabelas e o RLS estão íntegros.
2.  **Contratos de API:** Testa se todos os endpoints retornam o JSON esperado.
3.  **Fluxo E2E:** Simula um pedido do início ao fim (Frontend -> Backend -> KDS -> Pagamento).
4.  **Consistência Mobile:** Verifica se as Stores (Zustand) e o Cache (Dexie) estão sincronizados.

## 2. Protocolo de Bloqueio
Se o Omni-Check falhar em **qualquer** ponto, o Kernel Executor (`atualizar.py`) entrará em modo **READ_ONLY**. 
Nenhuma nova feature poderá ser injetada até que o erro de regressão seja sanado.

## 3. Próximos Passos Imediatos
1.  Execução da Task `TASK-QA-OMNI` (Criação do script mestre).
2.  Documentação de todas as telas (Dicionário de Páginas).
3.  Aplicação dos Questionários de 100 Perguntas para auditoria de vulnerabilidade cognitiva.

