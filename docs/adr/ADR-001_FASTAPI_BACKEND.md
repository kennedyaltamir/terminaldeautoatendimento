# ADR-001: Adoção de FastAPI como Backend Framework

**Status:** ACEITA
**Data:** Outubro de 2025
**Decisores:** CTO, Tech Lead

## Contexto
O MesaFlow necessita de um backend de alta performance, capaz de lidar com conexões assíncronas (WebSockets para KDS) e validação rigorosa de dados para operações financeiras e fiscais. A escolha do framework define a velocidade de desenvolvimento e a escalabilidade do sistema.

## Decisão
Adotamos **FastAPI (Python)** como o framework principal para o backend.

## Alternativas Consideradas

### 1. Django (Python)
- **Prós:** Baterias inclusas, ORM robusto, Admin nativo.
- **Contras:** Monolítico, síncrono por padrão (na época da decisão), overhead excessivo para microsserviços/APIs puras.
- **Motivo do Descarte:** Peso desnecessário e menor performance em I/O assíncrono comparado ao FastAPI.

### 2. Flask (Python)
- **Prós:** Simples, flexível.
- **Contras:** Falta de validação de dados nativa (Pydantic), suporte async não é cidadão de primeira classe.
- **Motivo do Descarte:** Necessidade de instalar muitas libs de terceiros para atingir o que o FastAPI oferece nativamente.

### 3. Node.js (Express/NestJS)
- **Prós:** Ecossistema vasto, mesma linguagem do frontend.
- **Contras:** Tipagem fraca (mesmo com TS, runtime é JS), callback hell potencial, gestão de threads para tarefas pesadas (CPU bound) é complexa.
- **Motivo do Descarte:** Python oferece melhor ecossistema para Data Science (futuro IA do MesaFlow) e tipagem forte com Pydantic.

## Consequências

### Positivas
- **Performance:** Uso de Starlette e Pydantic garante alta velocidade.
- **Produtividade:** Geração automática de OpenAPI (Swagger) reduz tempo de documentação.
- **Segurança:** Validação de tipos estrita reduz bugs de runtime.
- **Async:** Suporte nativo a `async/await` facilita integração com WebSockets e I/O de banco.

### Negativas
- **Curva de Aprendizado:** Exige conhecimento de Python moderno (Type Hints).
- **Ecossistema:** Menor que Django, exigindo seleção manual de libs para Auth, ORM (SQLAlchemy), etc.

## Compliance
Esta decisão está alinhada com os requisitos de performance (SLA < 200ms) e manutenibilidade do código.