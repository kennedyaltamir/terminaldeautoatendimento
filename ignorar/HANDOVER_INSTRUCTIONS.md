[[MESAFLOW_BEGIN:HANDOVER_INSTRUCTIONS.md]]
# 📦 Guia de Transferência de IA (Handover)

Siga estes passos exatos para transferir o projeto MesaFlow para uma nova instância de IA sem perder contexto.

## Passo 1: Organização Final
Garanta que todos os scripts e testes estejam nos lugares certos.
```bash
python scripts/maintenance/organize_scripts.py
```

## Passo 2: Geração de Contexto
Este comando vai ler todo o projeto (ignorando lixo e resumindo testes) e criar o arquivo `todososarquivos.txt`.
```bash
python gerartxt.py
```

## Passo 3: Configuração da Nova IA
1.  Abra um novo chat (Google AI Studio, ChatGPT, Claude).
2.  Procure a configuração de **System Instructions** (ou System Prompt).
3.  Copie o conteúdo do arquivo `docs/Prompts/System_Persona.xml` e cole lá.
    *   *Se a IA não tiver campo de System, cole na primeira mensagem.*

## Passo 4: O Prompt de Ativação
Na caixa de mensagem do chat, digite o seguinte (e anexe o `todososarquivos.txt`):

```text
Estou transferindo o projeto MesaFlow (SaaS B2B Híbrido).
O contexto completo do código, documentação e roadmap está no arquivo 'todososarquivos.txt' anexo.

Sua missão imediata é assumir a FASE 6 (Polimento & Escala).
Siga estritamente o protocolo definido em 'docs/Prompts/Master_Handover.xml'.

Se você leu o arquivo e entendeu a arquitetura, responda APENAS com a frase de ativação.
```

## Passo 5: Validação
A IA deve responder:
> "Estou preparada. Contexto carregado, arquitetura mapeada e pronta para a Fase 6. Pode enviar o código completo."

Se ela responder isso, a transferência foi um sucesso.
[[MESAFLOW_END]]

[[MESAFLOW_BEGIN:docs/Prompts/System_Persona.xml]]
<System_Persona version="3.0">
  <Identity>
    <Role>Arquiteto de Software Sênior (Fullstack) & Product Manager (SaaS B2B)</Role>
    <Name>MesaFlow Architect</Name>
    <Tone>Profissional, Técnico, Pragmático e Focado em Solução.</Tone>
    <Language>Português (BR)</Language>
  </Identity>

  <Context>
    Você é o guardião técnico do MesaFlow, um sistema operacional para restaurantes que combina:
    1. Autoatendimento (Totem/Kiosk e QR Code na Mesa).
    2. Operação (App do Garçom e KDS de Cozinha).
    3. Logística (Delivery e App do Entregador).
    4. Fintech (Split de Pagamento e Assinaturas).
  </Context>

  <Directives>
    <Rule id="1" priority="CRITICAL">
      **Entrega Integral:** NUNCA use placeholders como `// ...restante do código`. Envie arquivos completos.
    </Rule>
    <Rule id="2" priority="CRITICAL">
      **Protocolo de Automação:** Todo código deve ser encapsulado em:
      [[MESAFLOW_BEGIN:caminho/do/arquivo.ext]]
      ...conteúdo...
      [[MESAFLOW_END]]
    </Rule>
    <Rule id="3" priority="HIGH">
      **Classificação:** Inicie toda resposta declarando a complexidade: "TRIVIAL" ou "COMPLEXA".
    </Rule>
    <Rule id="4" priority="HIGH">
      **Testes:** Tasks COMPLEXAS exigem um arquivo de teste em `scripts/tests/`.
    </Rule>
    <Rule id="5" priority="MEDIUM">
      **Segurança:** Valide sempre `company_id` em queries e sanitize inputs HTML.
    </Rule>
  </Directives>

  <Knowledge_Base>
    - Stack: Python 3.11 (FastAPI), Next.js 14 (App Router), PostgreSQL, Redis.
    - Padrões: Factory Pattern (Pagamentos/Fiscal), Repository Pattern (implícito), Adapter Pattern.
    - Infra: Docker, Render.com, Neon.tech.
  </Knowledge_Base>
</System_Persona>
[[MESAFLOW_END]]
# 📦 Guia de Transferência de IA (Handover)

Siga estes passos exatos para transferir o projeto MesaFlow para uma nova instância de IA sem perder contexto.

## Passo 1: Geração de Contexto
Este comando vai ler todo o projeto (ignorando lixo e resumindo testes) e criar o arquivo `todososarquivos.txt`.
```bash
python gerartxt.py
```

## Passo 2: Configuração da Nova IA
1. Abra um novo chat (Google AI Studio, ChatGPT, Claude).
2. Procure a configuração de **System Instructions** (ou System Prompt).
3. Copie o conteúdo do arquivo `docs/Prompts/System_Instructions.xml` e cole lá.

## Passo 3: O Prompt de Ativação
Na caixa de mensagem do chat, digite o seguinte (e anexe o `todososarquivos.txt`):

```text
Estou transferindo o projeto MesaFlow (SaaS B2B Híbrido). 
O contexto completo do código, documentação e roadmap está no arquivo 'todososarquivos.txt' anexo.

Sua missão imediata é assumir a FASE 5 (Enterprise & Escala).
Siga estritamente o protocolo definido em 'docs/Prompts/Master_Handover.xml'.

Se você leu o arquivo e entendeu a arquitetura, responda APENAS com a frase de ativação.
```

## Passo 4: Validação
A IA deve responder:
> "Estou preparada, pode me enviar seu código completo."

Se ela responder isso, a transferência foi um sucesso.

# 📦 Guia de Transferência de IA (Handover)

Siga estes passos exatos para transferir o projeto MesaFlow para uma nova instância de IA sem perder contexto.

## Passo 1: Preparação do Ambiente
Certifique-se de que o servidor está rodando para que a IA possa ver o estado atual da UI.
```bash
python run.py
```

## Passo 2: Geração de Contexto (Código + Visual)
Este comando vai realizar uma auditoria visual (screenshots) e ler todo o projeto, criando o arquivo `todososarquivos.txt`.
```bash
python gerartxt.py
```

## Passo 3: Configuração da Nova IA
1. Abra um novo chat.
2. Copie o conteúdo do arquivo `docs/Prompts/System_Instructions.xml` e cole nas **System Instructions**.
3. Anexe o arquivo `todososarquivos.txt` gerado.
4. (Opcional mas Recomendado) Envie a pasta `screenshots/` compactada ou mencione que as imagens estão disponíveis para análise de layout.

## Passo 4: O Prompt de Ativação
Na caixa de mensagem do chat, digite:

```text
Estou transferindo o projeto MesaFlow. 
O contexto completo do código e a estrutura visual estão no arquivo 'todososarquivos.txt' anexo.

Sua missão imediata é assumir a FASE 6 (Polimento & Escala).
Siga estritamente o protocolo definido em 'docs/Prompts/Master_Handover.xml'.

Se você leu o arquivo e entendeu a arquitetura híbrida, responda APENAS com a frase de ativação.
```

## Passo 5: Validação
A IA deve responder:
> "Estou preparada, pode me enviar seu código completo."


# 📦 Guia de Transferência de IA (Handover)

Siga estes passos exatos para transferir o projeto MesaFlow para uma nova instância de IA sem perder contexto.

## Passo 1: Preparação do Ambiente
Certifique-se de que o servidor está rodando para que o script possa capturar o estado atual da interface.
```bash
python run.py
```

## Passo 2: Geração de Contexto (Código + Visual)
Execute o gerador v3.5. Ele vai tirar screenshots de todas as telas e consolidar o código no arquivo `todososarquivos.txt`.
```bash
python gerartxt.py
```

## Passo 3: Configuração da Nova IA
1. Abra um novo chat (Google AI Studio, ChatGPT Plus ou Claude 3.5).
2. Configure as **System Instructions** com o conteúdo de `docs/Prompts/System_Instructions.xml`.
3. Anexe o arquivo `todososarquivos.txt`.
4. (Opcional) Envie a pasta `screenshots/` compactada para análise visual.

## Passo 4: O Prompt de Ativação
Copie e cole a seguinte mensagem no chat:

```text
Estou transferindo o projeto MesaFlow (SaaS B2B Híbrido). 
O contexto completo do código, documentação e estrutura visual estão no arquivo 'todososarquivos.txt' anexo.

Sua missão imediata é assumir a FASE 6 (Polimento & Escala).
Siga estritamente o protocolo definido em 'docs/Prompts/Master_Handover.xml'.

Se você leu o arquivo e entendeu a arquitetura híbrida e os padrões de segurança, responda APENAS com a frase de ativação definida no protocolo.
```

## Passo 5: Validação
A IA deve responder:
> "Estou preparada. Contexto carregado, arquitetura mapeada e pronta para a Fase 6. Pode enviar o código completo."

Se ela responder isso, a transferência foi um sucesso.
