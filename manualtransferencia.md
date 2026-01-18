Este é o **Protocolo de Handoff Cognitivo (PHC)**. Ele foi desenhado para que a transferência de conhecimento entre você e uma nova IA ocorra com **zero perda de fidelidade** e **zero alucinação**.

Siga este manual sempre que for iniciar uma nova sessão ou trocar de ferramenta de IA.

---

# 📖 Manual de Handoff Soberano: MesaFlow OS

## Fase 1: Preparação (No seu terminal)
Antes de enviar os arquivos, você deve garantir que a "Verdade" está atualizada com o código mais recente.

1.  **Gere a Verdade Estrutural:**
    ```powershell
    python scripts/maintenance/systemic_truth_engine.py
    ```
    *Isso garante que o arquivo `project-ai-context.json` reflete exatamente o que está no disco agora.*

---

## Fase 2: O Pacote de Dados (O que enviar)
Você deve anexar ou colar o conteúdo de **4 arquivos fundamentais**. Eles são o "Kit de Sobrevivência" da nova IA:

1.  **`governance/prompts/AI_SYSTEM_INITIATION.xml`** (O DNA e as Leis).
2.  **`project-ai-context.json`** (O Grafo de Dependências e Fatos).
3.  **`project-ai-context.md`** (O Resumo Executivo e Hotspots).
4.  **`architecture.mmd`** (O Modelo Mental Visual).

---

## Fase 3: O Comando de Iniciação (O que digitar)
Copie e cole o texto abaixo como a **primeira mensagem** para a nova IA, anexando os arquivos citados acima:

> **"Você está sendo inicializado como a instância de Arquiteto Cognitivo Sênior do sistema MesaFlow OS.**
>
> **Siga rigorosamente o rito de boot definido no arquivo `AI_SYSTEM_INITIATION.xml` anexo.**
>
> **Instruções de Ingestão:**
> 1. Processe as **Leis Constitucionais** do XML.
> 2. Analise a **Fonte da Verdade** no `project-ai-context.json`.
> 3. Leia a **Narrativa Executiva** no `project-ai-context.md`.
>
> **Não tente adivinhar a lógica.** Use as métricas de *Blast Radius* e as *Issues* detectadas pelo scanner para compor seu entendimento.
>
> **Emita o bloco `<BOOT_COMPLETE>` conforme o contrato de output para prosseguirmos."**

---

## Fase 4: Validação do Handoff
A nova IA **DEVE** responder com um bloco XML parecido com este:

```xml
<BOOT_COMPLETE>
    <Context_Validation>
        <Detected_Domains>Frontend, Backend, Mobile, Fintech</Detected_Domains>
        <Critical_Files_Count>X</Critical_Files_Count>
    </Context_Validation>
    <Understanding_Summary>
        O MesaFlow OS é um sistema modular... (etc)
    </Understanding_Summary>
    ...
</BOOT_COMPLETE>
```

### 🚩 Sinais de Alerta (Se isso acontecer, a IA falhou):
*   Se ela responder: *"Olá! Como posso te ajudar com seu código hoje?"* (Ela ignorou o protocolo e está em modo "assistente genérico").
*   Se ela começar a sugerir mudanças sem citar o `project-ai-context.json`.
*   Se ela não emitir o bloco `<BOOT_COMPLETE>`.

**Nesses casos, responda:** *"Protocolo violado. Leia o AI_SYSTEM_INITIATION.xml e emita o BOOT_COMPLETE antes de qualquer ação."*

---

## Por que este manual funciona?
*   **Isolamento:** A IA não "chuta" como o projeto funciona; ela lê o grafo real.
*   **Autoridade:** O XML tira a IA da zona de conforto e a coloca em um papel de responsabilidade técnica.
*   **Eficiência:** Você economiza horas de explicação. O `project-ai-context.json` resume 300 mil linhas de código em um mapa de dependências que a IA lê em milissegundos.

**Agora, você está pronto para rodar os comandos finais e selar o sistema!** 🚀