# ⚖️ Governança de Missões: Domínio Mobile

## 1. Definição de Missão
Uma **Missão** no ecossistema MesaFlow é uma unidade de trabalho atômica, governada por um contrato de escopo rígido.

### 1.1 Atributos Obrigatórios
- **Camada Única:** Uma missão deve focar em apenas uma camada arquitetural (Infra, App, ou UI).
- **Objetivo Único:** Deve resolver um problema específico sem ramificações.
- **Escopo Explícito:** Definição clara do que deve ser feito (Positivo) e do que é proibido (Negativo/Blocker).
- **Encerramento Formal:** Uma missão só é concluída após validação de código, documentação e scripts de verificação.

## 2. Regras de Bloqueio (Blockers)
Para manter a integridade do projeto, os seguintes itens são **BLOCKERS** por padrão:

- **UI em Camadas Baixas:** É proibido criar arquivos `.tsx` ou componentes visuais em missões de Infraestrutura ou Aplicação.
- **Estado sem Contrato:** Nenhuma Store ou Contexto pode ser criado sem uma definição formal de tipos e lifecycle.
- **Acoplamento Prematuro:** Camadas de infraestrutura não devem conhecer camadas de UI ou Navegação.
- **Alucinação de Fases:** Antecipar funcionalidades de missões futuras sem autorização explícita.

## 3. Definition of Done (DoD)
Uma entrega só é aceita se contiver:
1. **Código:** Implementação completa e funcional.
2. **Documentação:** Registro da task e decisões em `docs/mobile/`.
3. **Validação:** Scripts Python ou testes automatizados que comprovem a entrega.
