# ADR-003: Render.com como Plataforma de Runtime

**Status:** ACEITA
**Data:** Novembro de 2025
**Decisores:** DevOps Team

## Contexto
Necessidade de uma plataforma de hospedagem (PaaS) para o backend Python que ofereça deploy contínuo (GitOps), SSL automático e facilidade de gestão, sem a complexidade de Kubernetes.

## Decisão
Adotamos **Render.com** para hospedagem do Backend e Workers.

## Alternativas Consideradas

### 1. AWS EC2 / ECS
- **Prós:** Controle total, custo baixo em escala massiva.
- **Contras:** Exige gestão de SO, patches, configuração de Load Balancer, Auto Scaling Groups.
- **Motivo do Descarte:** Overhead operacional inaceitável para o tamanho atual da equipe.

### 2. Heroku
- **Prós:** DX excelente.
- **Contras:** Preço proibitivo em escala, dormência de dynos, limitações de região.
- **Motivo do Descarte:** Custo.

### 3. Vercel (para Backend Python)
- **Prós:** Integração com Frontend.
- **Contras:** Limitações severas em Serverless Functions (timeout, tamanho de payload), inadequado para WebSockets persistentes.
- **Motivo do Descarte:** Incompatibilidade técnica com requisitos de WebSocket e Long-running tasks.

## Consequências

### Positivas
- **Simplicidade:** Deploy via `git push`.
- **Infra as Code:** Configuração via `render.yaml`.
- **Custo:** Previsível e competitivo.
- **Rede Privada:** Comunicação interna segura entre serviços.

### Negativas
- **Região:** Latência pode ser maior se o banco de dados não estiver na mesma região (Oregon/Frankfurt). Mitigado escolhendo região compatível com Neon.
- **Build Time:** Pode ser mais lento que CI dedicado.

## Compliance
O Render possui certificações SOC 2 e ISO 27001, alinhado com a política de Vendor Risk do MesaFlow.