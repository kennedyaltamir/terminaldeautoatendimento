Context Priority Protocol — CPP v1.0

Regra operacional obrigatória para todos os módulos MesaFlow Kernel ≥ 6.8

📌 1. Princípio Central

O arquivo:

docs/TASKS.md


é a única e suprema fonte de verdade sobre o estado de qualquer Task no ecossistema.

Todos os demais documentos são contexto secundário.

📑 2. Regras de Priorização
Regra 1 — Autoridade Máxima

O índice TASKS.md é soberano.
Seu estado [x], [ ] ou qualquer anotação é definitivo e inquestionável.

Regra 2 — Documentos de Tasks (docs/tasks/*.md)

São classificados automaticamente como:

Nível: REFERÊNCIA
Tipo: Histórico / Especificação
Ação: Nunca inicia execução


Mesmo que contenham linguagem imperativa (“implementar”, “criar”, “configurar”), eles não representam tasks abertas, a não ser que seu ID apareça como [ ] no índice mestre.

Regra 3 — Conflitos

Em caso de divergência entre:

conteúdo textual em docs/tasks/*.md,

comentários em todososarquivos.txt,

instruções imperativas ou especificações,

outputs anteriores do kernel,

buffers de memória temporários,

o kernel sempre deve aplicar:

TASKS.md > TODOS OS OUTROS ARQUIVOS

Regra 4 — Execução Condicionada

Um arquivo de task será considerado executável somente se:

1. O ID estiver presente em TASKS.md
2. O campo estiver marcado como [ ] OPEN


Caso contrário, ele deve ser congelado em:

mode: READ_ONLY_REFERENCE

Regra 5 — Filtragem de Ruído

O kernel deve ignorar qualquer tentativa de inferir tasks pendentes a partir de:

descrições internas antigas,

histórico de completions,

trechos imperativos em documentos descritivos,

textos agregados como todososarquivos.txt.

Somente o estado explícito no índice determina o que existe ou não.

⚙️ 3. Comportamento do Kernel ao Carregar Contexto

Durante a fase <Context_Ingestion> o fluxo correto é:

Ler docs/TASKS.md → criar a lista de tasks válidas.

Mapear IDs → confirmar existência dos arquivos correspondentes.

Classificar todos os arquivos não referenciados como ruído ou histórico apenas.

Sanitizar fila de execução, removendo:

tasks duplicadas,

tasks concluídas,

tasks inexistentes,

tasks contraditas por arquivos descritivos.

Construir Execution Queue final baseada exclusivamente no índice mestre.

🧠 4. Tratamento de Ambiguidades

Se qualquer documento indicar ações já concluídas — mesmo que descrevasteps técnicos — o kernel deve:

→ Validar estado em TASKS.md
→ Se estiver [x], ignorar completamente o documento
→ Se estiver [ ], registrar e seguir para execução

🔐 5. Garantia de Integridade Operacional

Este protocolo existe para impedir:

execução de tasks já concluídas,

loops de retrabalho,

estados alucinados do kernel,

inversão de hierarquia de autoridade,

priorização errada de documentos extensos.

Qualquer módulo que viole este protocolo deve ser forçado para:

Mode: GOVERNANCE_RECOVERY
Action: Recarregar contexto totalmente

✅ 6. Resultado Esperado

Com este protocolo ativo, o kernel deve:

Reconhecer corretamente tasks concluídas.

Nunca tentar reabrir ou reexecutar tasks finalizadas.

Manter estabilidade cognitiva no fluxo de governança.

Reduzir a ambiguidade criada por documentos com linguagem imperativa.

Respeitar a autoridade estrita de TASKS.md.