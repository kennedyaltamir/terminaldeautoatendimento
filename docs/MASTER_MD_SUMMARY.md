# 📖 Resumo Narrativo da Documentação MesaFlow
> **Gerado em:** 2026-01-18T08:27:19.648869
> **Escopo:** 703 documentos analisados.


## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-DOC-01`

### 📄 rollback_plan.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 specs.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 verification_plan.md
1. Abrir o README.md no VS Code Preview. 2. Validar se a leitura é fluida e se a stack descrita condiz com o repositório.

--- 

## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-ENV-01`

### 📄 rollback_plan.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 specs.md
As variáveis devem ser categorizadas para facilitar a manutenção:

--- 
### 📄 verification_plan.md
1. Executar `python scripts/setup/audit_env.py`. 2. Verificar se o relatório aponta corretamente as variáveis que faltam no seu ambiente local.

--- 

## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-FEAT-01`

### 📄 specs.md
Documentação técnica de suporte ao módulo.

--- 

## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-FEAT-02`

### 📄 specs.md
Interface de visualização pública para clientes aguardando retirada (estilo Fast Food).

--- 

## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-FEAT-03`

### 📄 specs.md
Documentação técnica de suporte ao módulo.

--- 

## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-FIN-03`

### 📄 rollback_plan.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 specs.md
O MesaFlow deve garantir a sustentabilidade do modelo SaaS através de duas fontes de receita:

--- 
### 📄 verification_plan.md
1. Executar `pytest scripts/scripts/tests/test_payment_split.py`. 2. Simular um pagamento via script e verificar o campo `marketplace_fee` no banco.

--- 

## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-GOV-10`

### 📄 checklist.md
Documentação técnica de suporte ao módulo.

--- 

## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-INT-01`

### 📄 rollback_plan.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 specs.md
Consolidar o guia de configuração para as quatro integrações pilares do ecossistema MesaFlow, garantindo que o lojista consiga ativar os serviços de forma autônoma.

--- 
### 📄 verification_plan.md
1. Seguir o manual para configurar uma conta de teste (Sandbox). 2. Rodar o script de validação de conectividade.

--- 

## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-MAINT-01`

### 📄 rollback_plan.md
Se um arquivo crítico for movido acidentalmente para a pasta ignorar e o sistema apresentar falhas de execução ou build.

--- 
### 📄 specs.md
Arquivos que poluem a raiz e dificultam a geração de contexto:

--- 
### 📄 verification_plan.md
1. Executar o comando: python scripts/maintenance/sanitize_repo.py. 2. Verificar visualmente se a pasta ignorar foi criada.

--- 

## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-MAINT-02`

### 📄 specs.md
O AIS deve verificar:

--- 

## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-MAINT-03`

### 📄 specs.md
O script deve automatizar o navegador para: 1. Realizar login administrativo.

--- 

## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-MAINT-04`

### 📄 specs.md
Como o aplicativo utiliza **Deep Linking** (configurado na TASK-039), o script utilizará comandos `adb` para forçar a navegação para rotas específicas e capturar o frame buffer do emulador.

--- 

## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-MAINT-05`

### 📄 specs.md
O MesaFlow utiliza Redis para:

--- 

## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-MOB-02`

### 📄 rollback_plan.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 specs.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 verification_plan.md
1. Iniciar o app. 2. Navegar para a tela de Garçom e validar o grid de mesas.

--- 

## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-MOB-FIX-01`

### 📄 rollback_plan.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 specs.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 verification_plan.md
1. Executar `python scripts/maintenance/mobile_doctor.py`. 2. Tentar rodar `cd mobile && npx expo start --clear`.

--- 

## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-UX-02`

### 📄 specs.md
O objetivo é transitar de uma interface "funcional/técnica" para uma experiência "Premium/SaaS".

--- 

## 📂 Diretorio: `archive/phase_10_hardening/docs/details/TASK-UX-03`

### 📄 specs.md
Documentação técnica de suporte ao módulo.

--- 

## 📂 Diretorio: `canonic`

### 📄 execution_report.md
| Script | Status | Tempo | Erro | | :--- | :---: | :---: | :--- |

--- 
### 📄 README.md
Estes scripts sobreviveram ao 'Great Filter' e constituem a ferramenta operacional confiável do sistema. | ID | Script | Status |

--- 

## 📂 Diretorio: `docs/adr`

### 📄 ADR-000_INDEX.md
Este documento lista todas as Architecture Decision Records (ADRs) do projeto. | ID | Título | Status | Data | Tags |

--- 
### 📄 ADR-001_FASTAPI_BACKEND.md
O MesaFlow necessita de um backend de alta performance, capaz de lidar com conexões assíncronas (WebSockets para KDS) e validação rigorosa de dados para operações financeiras e fiscais. A escolha do framework define a velocidade de desenvolvimento e a escalabilidade do sistema.

--- 
### 📄 ADR-002_NEON_POSTGRESQL.md
O sistema precisa de um banco de dados relacional robusto, compatível com PostgreSQL, que suporte escalabilidade elástica e reduza o overhead de gerenciamento de infraestrutura (backups, updates, scaling).

--- 
### 📄 ADR-003_RENDER_RUNTIME.md
Necessidade de uma plataforma de hospedagem (PaaS) para o backend Python que ofereça deploy contínuo (GitOps), SSL automático e facilidade de gestão, sem a complexidade de Kubernetes.

--- 
### 📄 ADR-004_DUAL_HEALTH_ENDPOINT.md
O sistema precisa ser monitorado por ferramentas externas (Load Balancers, UptimeRobot, Status Pages) que, por padrão, buscam o endpoint `/health` na raiz. A arquitetura original expunha apenas `/api/health`.

--- 
### 📄 ADR-005_SECURITY_HARDENING_STRATEGY.md
O MesaFlow opera em modelo Multi-tenant B2B, processando dados sensíveis. A segurança baseada apenas em código (filtros ORM) é propensa a erro humano. É necessário uma defesa em profundidade.

--- 

## 📂 Diretorio: `docs`

### 📄 API.md
O Sistema Operacional para Food Service e Ambientes de Alto Tráfego.

--- 

## 📂 Diretorio: `docs/architecture`

### 📄 DEPENDENCY_MAP.md
graph TD subgraph "API Layer"

--- 
### 📄 domain-separation.md
Para garantir a escalabilidade e a manutenibilidade do ecossistema MesaFlow, fica estabelecida a separação estrita entre os domínios de execução. Esta diretriz impede que alterações em uma plataforma (ex: Mobile) afetem inadvertidamente outra (ex: Web).

--- 
### 📄 EXTERNAL_SLA_MATRIX.md
| Serviço | SLA Alvo | Timeout | Estratégia de Fallback | | :--- | :---: | :---: | :--- |

--- 
### 📄 INFRASTRUCTURE_MAP.md
Visão lógica da distribuição dos serviços do MesaFlow OS.

--- 
### 📄 SYSTEM_MAP.md
graph TD subgraph "Client Layer"

--- 

## 📂 Diretorio: `docs`

### 📄 ARCHITECTURE.md
┌──────────────┐       ┌──────────────┐       ┌──────────────┐ │  Cliente     │       │   API Gateway│       │  Banco de    │

--- 

## 📂 Diretorio: `docs/audit`

### 📄 EXPECTED_BEHAVIOR_MATRIX.md
Este documento define o comportamento padrão esperado para **TODAS** as telas do sistema MesaFlow. Utilize esta matriz para validar se a realidade (o que acontece na tela) condiz com a especificação.

--- 
### 📄 FULL_ROUTE_MAP.md
| Rota | Descrição | Status | | :--- | :--- | :---: |

--- 
### 📄 INTERACTIVE_ELEMENTS_LIST.md
Este documento lista todos os pontos de interação detectados estaticamente no código. Use-o para validar se todos os botões, links e inputs estão mapeados e funcionais.

--- 
### 📄 KIOSK_QA_CHECKLIST.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 REPO_INVENTORY.md
O MesaFlow OS opera sob uma arquitetura **Monolito Modular Híbrido**, composta por três grandes domínios de aplicação interconectados: 1.  **Backend (API Gateway & Core Logic):** Python/FastAPI.

--- 
### 📄 UI_COVERAGE_REPORT.md
| Prioridade | Tela | Plataforma | Score | Status | | :--- | :--- | :--- | :--- | :--- |

--- 
### 📄 UI_PRIORITY_MATRIX.md
Esta matriz orienta o esforço de documentação e QA, classificando as telas por impacto no negócio e risco operacional.

--- 

## 📂 Diretorio: `docs`

### 📄 BACKLOG.md
Este documento lista 50 tarefas potenciais para evoluir o MesaFlow de um MVP para um SaaS robusto e comercializável.

--- 
### 📄 CHANGELOG.md
Endurecimento estrutural do Backend para prevenção de regressão humana e integridade de dados.

--- 

## 📂 Diretorio: `docs/commercial`

### 📄 ENTERPRISE_ONBOARDING.md
Este roteiro garante que uma nova operação de grande porte (ex: Estádio ou Rede de Franquias) entre no ar com 100% de sucesso.

--- 
### 📄 ENTERPRISE_PITCH.md
"O MesaFlow não é apenas um sistema de pedidos. Ele é uma plataforma transacional construída com o mesmo rigor de sistemas financeiros, garantindo que sua operação nunca pare e seus dados nunca vazem."

--- 
### 📄 EVENT_QUEUE_MANAGEMENT.md
Em estádios e festivais, 70% das vendas ocorrem nos intervalos. A fila física é a maior barreira de faturamento.

--- 
### 📄 EVENT_QUEUE_MANAGEMENT_GUIDE.md
Em eventos com mais de 5.000 pessoas, o gargalo não é a produção, mas a **captura do pedido**. Filas físicas geram desistência de compra (churn imediato) e erro humano no caixa.

--- 
### 📄 GO_LIVE_CHECKLIST_REAL.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 README_SALES_TECHNICAL.md
O MesaFlow não é apenas um CRUD de pedidos. É uma plataforma governada por **Automação L5**.

--- 
### 📄 WHITE_LABEL_PLAYBOOK.md
O MesaFlow permite que grandes redes operem com sua própria identidade visual.

--- 

## 📂 Diretorio: `docs`

### 📄 CONTRIBUTING.md
Padrões e processos para manter a qualidade do código do MesaFlow.

--- 

## 📂 Diretorio: `docs/cycles`

### 📄 CYCLE_IGS_BLUEPRINT.md
Com a fundação operacional (GTM) e a infraestrutura (Hardening) estabilizadas, o MesaFlow entra na fase de diferenciação competitiva através de Inteligência Artificial e Efeitos de Rede. O objetivo deste ciclo é transformar o MesaFlow de um "Sistema de Gestão" para uma "Plataforma de Inteligência", onde os dados geram valor tangível (previsão de vendas) e a rede de usuários gera retenção (Passport).

--- 

## 📂 Diretorio: `docs`

### 📄 DELIVERY_IMPROVEMENTS.md
Este documento detalha 10 melhorias estratégicas para transformar o módulo de entregas do MesaFlow em uma solução de logística de classe mundial ("Uber-like").

--- 
### 📄 DEPLOY.md
Este guia cobre o deploy da stack **FastAPI + PostgreSQL**.

--- 
### 📄 DEVOPS.md
Este documento descreve como o código sai da sua máquina e chega aos servidores de produção (Render/Vercel) com segurança.

--- 
### 📄 DOCUMENTATION_INDEX.md
This report represents the **single source of truth** of the current database schema.

--- 

## 📂 Diretorio: `docs/enterprise`

### 📄 AUDIT_EXPORT_GUIDE.md
O MesaFlow fornece um endpoint seguro para exportação em lote de logs de auditoria. Os dados são fornecidos em formato **CSV (Comma Separated Values)**, compatível com a maioria das ferramentas de SIEM (Splunk, ELK, Datadog) e planilhas (Excel, Google Sheets).

--- 
### 📄 COMPLIANCE_MAPPING.md
Este documento mapeia os controles técnicos e administrativos do MesaFlow para os frameworks de segurança mais exigidos pelo mercado Enterprise. Utilize esta matriz para preenchimento rápido de questionários de segurança (SIG, VSA, CAIQ).

--- 
### 📄 DR_BCP_PLAN.md
Este documento estabelece as diretrizes, procedimentos e responsabilidades para garantir a continuidade das operações críticas do **MesaFlow** em caso de interrupções severas ou desastres. O plano cobre:

--- 
### 📄 DUE_DILIGENCE_REPORT.md
O MesaFlow é uma plataforma SaaS orientada a operações críticas de restaurantes, com foco em integridade financeira, isolamento multi-tenant e governança técnica auditável. O sistema foi projetado desde sua base para suportar auditorias técnicas e escalabilidade progressiva.

--- 

## 📂 Diretorio: `docs/enterprise/evidence_pack`

### 📄 ARCHITECTURE_OVERVIEW.md
O MesaFlow opera sob uma arquitetura de **Monolito Modular Híbrido**, otimizada para consistência de dados e baixa latência operacional.

--- 
### 📄 AVAILABILITY_AND_SLA.md
O MesaFlow compromete-se com um **Uptime Mensal de 99,9%** para os serviços críticos da plataforma.

--- 
### 📄 DATA_PROTECTION_AND_LGPD.md
O tratamento de dados pessoais na plataforma é realizado sob as bases legais de:

--- 
### 📄 ENTERPRISE_EVIDENCE_INDEX.md
Este pacote consolida a documentação técnica, de segurança e conformidade do MesaFlow para fins de auditoria, *due diligence* e *procurement* corporativo.

--- 
### 📄 INCIDENT_RESPONSE.md
| Nível | Descrição | Exemplo | | :--- | :--- | :--- |

--- 
### 📄 SECURITY_OVERVIEW.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 VENDOR_AND_SUBPROCESSORS.md
O MesaFlow utiliza uma cadeia de fornecedores de classe mundial para garantir a segurança, disponibilidade e performance da plataforma. Todos os sub-processadores passam por rigorosa avaliação de risco.

--- 

## 📂 Diretorio: `docs/enterprise`

### 📄 EVIDENCE_PACK.md
Este documento consolida as evidências técnicas, de segurança e governança do **MesaFlow OS**, demonstrando nossa capacidade de atender aos requisitos de grandes corporações (Enterprise), processos de *procurement* e auditorias de *due diligence*. O MesaFlow opera sob uma arquitetura **Monolito Modular Híbrido**, projetada para alta disponibilidade (99.9% SLA), segurança em profundidade (Defense in Depth) e conformidade regulatória (LGPD).

--- 
### 📄 GO_LIVE_CERTIFICATE.md
Este documento certifica que o sistema **MesaFlow** passou pelos ritos de governança e auditoria técnica necessários para operação comercial.

--- 
### 📄 VENDOR_RISK_ASSESSMENT.md
Este documento detalha a análise de risco da cadeia de suprimentos de dados do MesaFlow. Todos os fornecedores listados foram avaliados quanto à sua postura de segurança, conformidade regulatória e criticidade para a operação.

--- 

## 📂 Diretorio: `docs`

### 📄 EXECUTIVE_SUMMARY.md
O MesaFlow OS é uma infraestrutura operacional de missão crítica para ambientes de alta rotatividade (Food Service, Hotelaria, Eventos). O sistema substitui processos fragmentados por uma orquestração digital onde o **pagamento é o trigger causal** que sincroniza cliente, staff e logística em tempo real.

--- 

## 📂 Diretorio: `docs/frontend`

### 📄 DESIGN_SYSTEM.md
Documentação técnica de suporte ao módulo.

--- 

## 📂 Diretorio: `docs`

### 📄 FRONTEND_STRUCTURE.md
Este documento descreve a estrutura do cliente web desenvolvido em **Next.js 14 (App Router)** com **Tailwind CSS**.

--- 
### 📄 GTM_CHECKLIST.md
This document outlines the critical gaps identified for the 2026 GTM launch based on the current repository state.

--- 
### 📄 GUIA_HARDWARE.md
Requisitos técnicos para rodar o MesaFlow com estabilidade.

--- 
### 📄 GUIA_STRIPE_ASSINATURAS.md
Este guia detalha como configurar sua conta no Stripe para ativar a cobrança automática de mensalidades no MesaFlow.

--- 
### 📄 IMPLEMENTATION_HISTORY.md
Documentação técnica de suporte ao módulo.

--- 

## 📂 Diretorio: `docs/improvements`

### 📄 GERARTXT_CAPABILITIES.md
Este documento cataloga as funcionalidades atuais da ferramenta de geração de contexto e as melhorias planejadas para as próximas versões.

--- 
### 📄 GERARTXT_UPGRADES.md
Lista de funcionalidades planejadas para a versão 3.0 do script de contexto. 1.  **Estimativa de Tokens:** Exibir contagem estimada (`chars / 4`) ao final.

--- 
### 📄 GERARTXT_V5_1_UPGRADE.md
1.  **Bloqueio de Binários (Ironclad Filtering):**

--- 
### 📄 GERARTXT_V5_UPGRADE.md
1.  **Priority Sorting (Primacy Effect):**

--- 
### 📄 GERARTXT_V6_UPGRADE.md
1.  **Git Delta (--changed):** Agora você pode gerar contexto apenas dos arquivos que modificou. Perfeito para correções rápidas. 2.  **Dependency Graph:** O script mapeia quem importa quem, ajudando a IA a entender a hierarquia de chamadas.

--- 
### 📄 UX_UI_MASTER_PLAN.md
1.  **Grupo A (Conversão & Identidade):** Login, Registro, Cardápio Público. 2.  **Grupo B (Operação Crítica):** KDS, App Garçom.

--- 

## 📂 Diretorio: `docs`

### 📄 INTEGRATION_HUB_GUIDE.md
O MesaFlow notifica sistemas externos sobre eventos em tempo real.

--- 

## 📂 Diretorio: `docs/investors`

### 📄 INVESTOR_QA_HOSTILE.md
Além disso, Python nos dá acesso nativo às melhores bibliotecas de IA/ML (Scikit, Pandas) para o nosso roadmap de previsão de demanda. Reescrever em Go agora seria otimização prematura. O Instagram e o Shopify escalaram com Python/Ruby.

--- 
### 📄 INVESTOR_REPORT_L5.md
O MesaFlow atingiu o nível de maturidade tecnológica **L5 (Self-Correcting)**. Isso significa que a plataforma não depende mais de intervenção humana para garantir a qualidade do código, segurança ou estabilidade operacional. O sistema é governado por IA e pipelines automatizados.

--- 
### 📄 PITCH_DECK_L5.md
Em ambientes de alto tráfego (Estádios, Food Halls, Redes de Fast Food), a fricção operacional mata a margem de lucro.

--- 
### 📄 TECH_DUE_DILIGENCE.md
O MesaFlow Mobile não é apenas um aplicativo, é uma plataforma de operação crítica governada por inteligência artificial. Atingimos o nível de maturidade **L5 (Self-Correcting)**, onde o sistema é capaz de detectar, validar e impedir regressões de forma autônoma.

--- 

## 📂 Diretorio: `docs/legal`

### 📄 APPLE_REVIEW_PLAYBOOK.md
Este guia contém as respostas exatas para o formulário do App Store Connect.

--- 
### 📄 DATA_BREACH_NOTIFICATION.md
Esta política descreve os procedimentos do MesaFlow em caso de incidente de segurança que resulte em acesso não autorizado, vazamento ou comprometimento de dados pessoais.

--- 
### 📄 GOOGLE_DATA_SAFETY_PLAYBOOK.md
Respostas para o formulário de Segurança de Dados no Google Play Console.

--- 
### 📄 MOBILE_PRIVACY_POLICY.md
Esta política descreve como o aplicativo MesaFlow trata dados em dispositivos móveis.

--- 
### 📄 PRIVACY_POLICY.md
O MesaFlow está comprometido com a proteção de dados e a conformidade com a Lei Geral de Proteção de Dados (LGPD - Lei nº 13.709/2018).

--- 
### 📄 RoPA.md
Este documento mapeia o ciclo de vida dos dados pessoais dentro da plataforma MesaFlow.

--- 
### 📄 SECURITY_DISCLOSURE.md
O MesaFlow valoriza a comunidade de segurança e encoraja a divulgação responsável de vulnerabilidades. Esta política define as regras para pesquisadores de segurança (White Hat Hackers) que desejam testar e reportar falhas em nossos sistemas.

--- 
### 📄 SLA.md
Este documento define os compromissos de disponibilidade e suporte técnico da plataforma MesaFlow para clientes dos planos **Pro** e **Enterprise**.

--- 
### 📄 STORE_DATA_SAFETY.md
Este documento serve como referência técnica para o preenchimento dos formulários de privacidade da **Google Play Store** e **Apple App Store**.

--- 
### 📄 SUBPROCESSORS.md
Para fornecer nossos serviços, o MesaFlow utiliza parceiros terceirizados ("Sub-processadores") para processar dados em nosso nome. Esta lista é mantida atualizada para garantir transparência e conformidade com a LGPD e outras leis de proteção de dados.

--- 
### 📄 TERMS_OF_SERVICE.md
Documentação técnica de suporte ao módulo.

--- 

## 📂 Diretorio: `docs/management`

### 📄 BUSINESS_MODEL_CANVAS.md
Define quem faz o que no projeto MesaFlow.

--- 
### 📄 CHANGE_MANAGEMENT_PLAN.md
Qualquer alteração significativa no escopo (novas features não planejadas, mudança de arquitetura) deve seguir este fluxo: 1.  **Origem:** Stakeholder ou Time identifica a necessidade.

--- 
### 📄 LESSONS_LEARNED.md
1.  **Mobile First:** Qualquer nova feature operacional deve ser desenhada primeiro para a tela do celular. 2.  **Observabilidade:** Logs estruturados são vitais. O `LoggerService` deve ser expandido.

--- 
### 📄 PLAYBOOK_30_DAYS.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 PLAYBOOK_72H.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 PLAYBOOK_90_DAYS.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 PLAYBOOK_EXECUTION.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 PROJECT_CHARTER.md
O setor de Food Service enfrenta um gargalo crítico: a fricção entre o desejo do cliente e a capacidade de atendimento da cozinha. Sistemas legados são fragmentados (um para PDV, um para KDS, um para Delivery).

--- 
### 📄 PROJECT_SCHEDULE.md
| Fase | Descrição | Início | Fim Estimado | Status | |:---|:---|:---:|:---:|:---:|

--- 
### 📄 PROJECT_STATUS_REPORT_TEMPLATE.md
| Indicador | Status | Comentário | |:---|:---:|:---|

--- 
### 📄 RISK_REGISTER.md
Este documento monitora ameaças potenciais ao sucesso do MesaFlow e define planos de mitigação. | ID | Risco | Probabilidade | Impacto | Severidade | Plano de Mitigação | Status |

--- 
### 📄 STAKEHOLDER_REGISTER.md
Mapeamento de quem impacta ou é impactado pelo MesaFlow.

--- 

## 📂 Diretorio: `docs`

### 📄 MANUAL_COZINHA.md
O **KDS (Kitchen Display System)** substitui as impressoras de papel. Ele organiza os pedidos por ordem de chegada e prioridade.

--- 
### 📄 MANUAL_DELIVERY.md
Este guia explica como operar o módulo de entregas do MesaFlow, desde o cadastro da frota até a entrega final ao cliente.

--- 
### 📄 MANUAL_FINANCEIRO.md
Este documento detalha a operação, configuração e fluxo de caixa das funcionalidades financeiras do sistema. O MesaFlow foi desenhado para ser uma **Fintech Embutida**, gerando receita tanto para o restaurante quanto para a plataforma (SaaS).

--- 
### 📄 MANUAL_GESTOR.md
Bem-vindo ao MesaFlow! Este guia foi desenhado para ajudar você, proprietário ou gerente, a configurar sua loja para vender mais e operar com eficiência máxima.

--- 
### 📄 MANUAL_PAGAMENTOS.md
O MesaFlow possui um sistema híbrido de pagamentos que suporta dois modos de operação. Este documento explica como alternar entre eles.

--- 

## 📂 Diretorio: `docs/manual_testing`

### 📄 FUNCTIONAL_TEST_TEMPLATE.md
| Página | Ação Testada | Resultado Esperado | Funcionou? | Observações/Erros | | :--- | :--- | :--- | :---: | :--- |

--- 

## 📂 Diretorio: `docs/manuals`

### 📄 DEPLOYMENT_PLAN.md
Este documento guia a instalação do MesaFlow em um novo ambiente de produção.

--- 
### 📄 DIGITAL_CERTIFICATE_GUIDE.md
Para emitir Notas Fiscais (NFC-e) pelo MesaFlow via Focus NFe, sua empresa precisa de um **Certificado Digital e-CNPJ tipo A1**.

--- 
### 📄 FISCAL_INTEGRATION_MASTER_GUIDE.md
Este documento é o guia definitivo para configuração, homologação e operação do módulo fiscal do MesaFlow OS.

--- 
### 📄 FISCAL_TOKEN_SETUP.md
Este documento descreve o processo para obter e configurar a credencial necessária para a emissão de NFC-e no MesaFlow OS.

--- 
### 📄 IFOOD_INTEGRATION_GUIDE.md
Este guia descreve como conectar sua loja do iFood ao MesaFlow para receber pedidos automaticamente no KDS.

--- 
### 📄 IFOOD_SETUP_GUIDE.md
Este guia orienta a obtenção das credenciais necessárias para integrar sua loja do iFood ao MesaFlow OS.

--- 
### 📄 MOBILE_LAUNCH_GUIDE.md
Se o emulador abriu mas você não vê o ícone do "MesaFlow", é porque em modo de desenvolvimento usamos o **Expo Go** como hospedeiro.

--- 
### 📄 MOBILE_SUCCESS_REPORT.md
O aplicativo MesaFlow Mobile foi inicializado com sucesso no seu emulador. Este é um marco crítico para a Fase 10.

--- 
### 📄 MOBILE_TESTING_GUIDE_ANDROID.md
Este guia detalha como compilar, instalar e validar as funcionalidades da TASK-MOB-02 utilizando o seu ambiente Android Studio.

--- 
### 📄 PUBLIC_MONITOR_GUIDE.md
O Monitor Público é uma interface de alta visibilidade projetada para ser exibida em TVs ou monitores voltados para o cliente no salão ou balcão de retirada.

--- 
### 📄 QUICK_START.md
Este guia contém os comandos essenciais para operar o ambiente de desenvolvimento do MesaFlow.

--- 
### 📄 REDESIGN_VISUAL_GUIDE.md
Este documento detalha as mudanças visuais e comportamentais introduzidas pelo "Enterprise Revamp".

--- 
### 📄 STABILIZATION_REPORT_JAN_2026.md
1. **Geração de Contexto:** Ao rodar `python gerartxt.py`, o arquivo `todososarquivos.txt` agora incluirá o código do aplicativo mobile, permitindo que a IA realize manutenções em todo o ecossistema simultaneamente. 2. **Segurança de Patches:** O `atualizar.py` agora é mais tolerante a ruídos de conversação, mas mantém a proibição estrita de omissões (``).

--- 
### 📄 TESTE_VOZ_RAPIDO.md
Como o seu ambiente já está rodando (`python run.py`) e você já gerou um pedido pago (`simular_pagamento.py`), siga os passos abaixo para validar a funcionalidade de voz.

--- 
### 📄 USER_GUIDE_MASTER.md
Bem-vindo ao ecossistema MesaFlow. Este manual consolida as instruções operacionais para todos os perfis de usuário.

--- 

## 📂 Diretorio: `docs`

### 📄 MASTER_CONTEXT.md
O **MesaFlow** é um ecossistema SaaS B2B Enterprise projetado para orquestrar operações em ambientes de alto tráfego (Restaurantes, Hotéis, Estádios e Eventos).

--- 
### 📄 MASTER_DOCUMENTATION_SUMMARY.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 MASTER_PROJECT_BIBLE.md
O MesaFlow é um Sistema Operacional (SaaS) para ambientes de alto tráfego (Restaurantes, Hotéis, Estádios). Diferente de cardápios digitais passivos, ele atua como um orquestrador de operações em tempo real.

--- 
### 📄 MESAFLOW_CONCEPT.md
Este documento descreve a lógica de funcionamento do ecossistema MesaFlow, detalhando os atores, fluxos e regras que regem a plataforma.

--- 

## 📂 Diretorio: `docs/mobile/architecture`

### 📄 APP_ARCHITECTURE.md
O padrão adotado é uma **Arquitetura em Camadas inspirada em Clean Architecture**, adaptada para o contexto pragmático de aplicações Mobile em React Native. 1.  **UI Layer (Screens/Components):** Componentes React puros e hooks de interface.

--- 
### 📄 DESIGN_SYSTEM.md
O MesaFlow Mobile adota uma estética **Dark-First**, priorizando alto contraste, legibilidade em ambientes de baixa luz (cozinhas/bares) e foco em ações rápidas.

--- 
### 📄 INTEGRATION_STRATEGY.md
O App Mobile comunica-se com o Backend (FastAPI) através de dois canais principais:

--- 
### 📄 MOBILE_ARCHITECTURE.md
O aplicativo móvel do MesaFlow é projetado para oferecer a melhor experiência operacional para Garçons, Cozinheiros e Entregadores, utilizando tecnologias nativas para garantir performance, acesso a hardware (impressoras, vibração) e notificações em tempo real.

--- 

## 📂 Diretorio: `docs/mobile/decisions`

### 📄 DATA_STRATEGY.md
O MesaFlow é um sistema multi-dispositivo. A política oficial de resolução de conflitos é:

--- 
### 📄 FUNCTIONAL_MAPPING.md
| Funcionalidade | Web Admin | App Mobile | Prioridade Mobile | | :--- | :---: | :---: | :--- |

--- 
### 📄 JWT_BACKEND_AUDIT.md
O backend MesaFlow emite tokens compatíveis com o padrão OpenID Connect, contendo as claims necessárias para o endurecimento semântico do mobile.

--- 
### 📄 MISSION_GOVERNANCE.md
Uma **Missão** no ecossistema MesaFlow é uma unidade de trabalho atômica, governada por um contrato de escopo rígido.

--- 

## 📂 Diretorio: `docs/mobile`

### 📄 ENTERPRISE_STORE_CHECKLIST.md
Este documento define os critérios mínimos para que um binário MesaFlow seja submetido para revisão oficial.

--- 
### 📄 PRINTER_HOMOLOGATION_GUIDE.md
Este guia orienta o teste de hardware real utilizando o binário nativo do MesaFlow.

--- 
### 📄 README.md
Este diretório centraliza toda a inteligência, histórico e especificações do aplicativo nativo MesaFlow (React Native / Expo).

--- 

## 📂 Diretorio: `docs/mobile/reports`

### 📄 CREDENTIALS_APPLE_GOOGLE.md
Para que o pipeline de CI/CD (`mobile_ci_cd.yml`) possa compilar e enviar o aplicativo para as lojas, as seguintes credenciais devem ser configuradas como **Secrets** no GitHub ou EAS.

--- 
### 📄 DIAGNOSTIC_REPORT.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 FINAL_HANDOFF_L5.md
O domínio Mobile atingiu o nível de maturidade **L5 (Enterprise Optimized)**. O código fonte, a infraestrutura de build e os protocolos de governança estão congelados e validados.

--- 

## 📂 Diretorio: `docs/mobile/reports/full_audit`

### 📄 FULL_L6_REPORT_093726.md
| ID | Teste | Status | Tempo | |---|---|---|---|

--- 

## 📂 Diretorio: `docs/mobile/reports`

### 📄 HUMAN_OBSERVATION_REPORT.md
| Tela | Erro | Auto-Fix Aplicado? | Resultado | |---|---|---|---|

--- 
### 📄 HUMAN_UI_TEST_REPORT.md
| Cenário | Status | Detalhes | |:---|:---:|:---|

--- 

## 📂 Diretorio: `docs/mobile/reports/login_audit`

### 📄 L6_FORENSIC_REPORT_093436.md
| ID | Teste | Status | Tempo | |---|---|---|---|

--- 

## 📂 Diretorio: `docs/mobile/reports`

### 📄 MESAFLOW_AUTO_GOVERNANCE_AI.md
You are an Enterprise Mobile Systems AI operating under the MESAFLOW Kernel and the INDA protocol.

--- 
### 📄 MOBILE_LOCAL_RUN.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 PRODUCTION_LOCK_MOBILE.md
O aplicativo MesaFlow Mobile foi submetido a rigorosos testes de integridade e encontra-se apto para distribuição. | Critério | Status | Evidência |

--- 

## 📂 Diretorio: `docs/mobile/setup`

### 📄 CREDENTIALS_APPLE_ENTERPRISE.md
Para empresas, você **NÃO** deve usar conta pessoal. 1. Acesse: [developer.apple.com/enroll](https://developer.apple.com/enroll).

--- 
### 📄 CREDENTIALS_GOOGLE_PLAY_ENTERPRISE.md
1. Acesse: [play.google.com/console](https://play.google.com/console). 2. Faça login com uma conta Google corporativa (recomendado).

--- 
### 📄 CREDENTIALS_REPORT.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ENVIRONMENT_SETUP.md
Este documento define o padrão de configuração de variáveis de ambiente para o aplicativo MesaFlow Mobile, garantindo segurança e conformidade com as lojas (Apple/Google).

--- 
### 📄 LOCAL_BUILD_GUIDE.md
Este guia descreve como gerar o APK utilizando os recursos da sua máquina local, integrando o fluxo do Expo com o Android Studio.

--- 
### 📄 SENTRY_GUIDE.md
Este documento orienta a obtenção e configuração das credenciais de telemetria exigidas pela Apple e Google para aplicativos Enterprise.

--- 

## 📂 Diretorio: `docs/mobile/tasks`

### 📄 00_DOCS_PLAN.md
Documentos a serem criados nas próximas iterações: 1.  **UI/UX Styleguide Mobile:** Definição de componentes nativos e padrões de toque.

--- 
### 📄 mobile_10_3_upgrade_sdk_54.md
Detectada incompatibilidade entre o ambiente de desenvolvimento (SDK 51) e a versão do cliente Expo Go disponível nas lojas (SDK 54). O upgrade é necessário para permitir o teste em dispositivos físicos.

--- 
### 📄 mobile_11_auth_infra.md
Implementação da camada de rede e segurança para o App Mobile, focando na persistência de tokens JWT e na renovação automática (Refresh Token) com controle de concorrência.

--- 
### 📄 mobile_12_auth_application.md
Após a consolidação da infraestrutura de rede (Missão 11), esta missão implementa o gerenciamento de estado global de autenticação, servindo como a ponte lógica para a futura interface de usuário.

--- 
### 📄 mobile_13_navigation_bootstrap.md
Materialização do fluxo de navegação do aplicativo, conectando a Store de Autenticação (`useAuthStore`) ao container de navegação nativo. O objetivo é criar um sistema reativo onde a UI transita automaticamente baseada no status da sessão.

--- 
### 📄 mobile_14_auth_semantics.md
A missão elevou a segurança do App Mobile, tornando-o consciente do ciclo de vida real dos tokens JWT.

--- 
### 📄 mobile_14a_semantic_auth.md
Implementação do endurecimento da camada de autenticação. O estado da sessão agora é derivado da integridade semântica e temporal do JWT (Access Token), garantindo que o App não opere com credenciais expiradas.

--- 
### 📄 mobile_14b_auth_boundary.md
Criação da barreira de renderização soberana do aplicativo. O objetivo é garantir que a árvore de componentes operacional (`AppStack`) nunca seja montada sem um estado de sessão validado temporal e matematicamente.

--- 
### 📄 mobile_15_ui_foundation.md
A UI Foundation do MesaFlow Mobile foi construída sob o princípio de **Pure UI**. Os componentes são burros (stateless em relação ao negócio), agnósticos ao contexto de autenticação e focados puramente em renderização baseada em propriedades.

--- 
### 📄 mobile_16_ui_implementation.md
Com a fundação do Design System concluída, esta missão foca na montagem das primeiras telas funcionais do aplicativo, conectando a interface ao estado global de autenticação.

--- 
### 📄 mobile_16_ui_login_home.md
Transição da infraestrutura mobile para a interface funcional real. Implementação das telas de Login e Home utilizando o Design System técnico (Tokens + UI Foundation).

--- 
### 📄 mobile_17_kds_orders.md
Implementação da primeira funcionalidade operacional nativa. O foco é a listagem e progressão de pedidos ativos, validando o consumo de APIs protegidas pelo fluxo de autenticação semântica.

--- 
### 📄 mobile_18_realtime_kds.md
Implementação da infraestrutura de comunicação em tempo real para o Monitor de Produção, garantindo latência sub-segundo na atualização de status e sincronia entre dispositivos nativos e web.

--- 
### 📄 mobile_19_operational_identity.md
Implementação da camada soberana de contexto operacional, eliminando dependências implícitas e valores fixos no aplicativo mobile.

--- 
### 📄 mobile_20_resilience_state_sync.md
Garantir a continuidade da operação do KDS Mobile em ambientes de rede instáveis, implementando recuperação automática de conexão e consistência de dados em tempo real.

--- 
### 📄 mobile_21_sla_engine.md
Elevação do KDS Mobile para um sistema de decisão por prioridade temporal. O tempo passa a ser um dado de domínio processado centralmente.

--- 
### 📄 mobile_22_operational_alerts.md
Implementação da camada de "Atenção Ativa" no KDS Mobile. O sistema interrompe o operador em momentos de criticidade temporal (SLA).

--- 
### 📄 mobile_23_operator_controls.md
Implementação da agência do operador sobre o sistema de alertas. O objetivo é permitir que o KDS Mobile seja silenciado em momentos de alta demanda ou por preferência da praça de produção, mantendo a integridade visual do SLA.

--- 
### 📄 mobile_24_resilience_recovery.md
Implementação da camada de confiabilidade para o KDS Mobile. Em ambientes de restaurante, quedas de Wi-Fi são comuns. O sistema deve garantir que, ao recuperar a conexão, o estado local seja imediatamente reconciliado com o servidor, evitando que o operador trabalhe com dados desatualizados.

--- 
### 📄 mobile_25_error_states.md
Implementação da transparência operacional no KDS Mobile. O sistema deve comunicar falhas de rede e de backend de forma proativa, garantindo que o operador não tome decisões baseadas em dados obsoletos sem saber que a sincronia está interrompida.

--- 
### 📄 mobile_26_local_persistence.md
Implementação do suporte offline real para o KDS Mobile. O objetivo é garantir que o aplicativo seja resiliente a reinicializações em ambientes sem conectividade, exibindo o último estado válido dos pedidos imediatamente após o boot.

--- 
### 📄 mobile_27_observability.md
Implementação da camada de inteligência de logs para o App Mobile. Em operações críticas de cozinha, falhas silenciosas são o pior cenário. O sistema agora registra eventos vitais, permitindo auditoria técnica e suporte proativo.

--- 
### 📄 mobile_28_release_candidate.md
Esta missão marca a conclusão da **Fase 10 (Mobile & Deep Tech)**. O aplicativo KDS Mobile atingiu a maturidade necessária para operação real, com todas as camadas de infraestrutura, inteligência de SLA e resiliência validadas.

--- 
### 📄 mobile_29a_pos_foundation.md
Início da transição das funcionalidades de atendimento do PWA para o App Nativo. Esta missão foca na infraestrutura de estado e na interface de seleção de mesas, permitindo que o garçom visualize o status do salão em tempo real.

--- 
### 📄 mobile_29b_order_entry.md
Implementação da funcionalidade core do Mobile POS: a capacidade de lançar itens em uma comanda. Esta missão conecta a seleção de mesas à navegação no cardápio e gestão de um carrinho de compras nativo.

--- 
### 📄 mobile_29c_order_submission.md
Finalização do fluxo de atendimento nativo. Esta missão implementa a tela de revisão do carrinho e a integração com o backend para persistência do pedido, garantindo que o garçom possa concluir a venda de forma segura e rápida.

--- 
### 📄 mobile_30a_printer_foundation.md
Implementação da camada de inteligência para emissão de tickets físicos. O Mobile POS agora é capaz de converter pedidos em comandos binários ESC/POS, preparando o terreno para a integração direta com hardware Bluetooth.

--- 
### 📄 mobile_30b_bluetooth_integration.md
Implementação da comunicação real com hardware de impressão. O aplicativo agora possui a inteligência para escanear o ambiente, identificar impressoras térmicas e persistir a escolha do operador para uso contínuo.

--- 
### 📄 mobile_31_push_notifications.md
Implementação da comunicação assíncrona entre o servidor e o aplicativo mobile. O objetivo é garantir que o staff receba alertas operacionais (ex: "Pedido Pronto", "Chamado de Mesa") mesmo quando o aplicativo não está em primeiro plano, aumentando a eficiência da operação.

--- 
### 📄 mobile_32_waiter_calls.md
Implementação da funcionalidade de atendimento reativo. O garçom agora pode visualizar e gerenciar solicitações de serviço (ajuda, conta, limpeza) feitas pelos clientes via QR Code, integrando o fluxo de salão ao sistema de tempo real.

--- 
### 📄 mobile_33_native_payments.md
Implementação da funcionalidade de recebimento financeiro no Mobile POS. O garçom agora pode fechar a conta de uma mesa e apresentar o QR Code Pix dinâmico diretamente no seu dispositivo, eliminando a necessidade de o cliente escanear o QR Code fixo da mesa novamente para pagar.

--- 
### 📄 mobile_34_offline_queue.md
Implementação da resiliência de venda para o Mobile POS. Em ambientes de salão, o Wi-Fi pode oscilar. O garçom deve ser capaz de concluir o lançamento do pedido mesmo sem rede, confiando que o sistema realizará a entrega assim que a conexão retornar.

--- 
### 📄 mobile_35_production_prep.md
Transição do ambiente de desenvolvimento para o ciclo de release de produção. Esta missão configura as ferramentas necessárias para gerar binários nativos e define os metadados obrigatórios para publicação nas lojas Apple App Store e Google Play Store.

--- 
### 📄 mobile_36_native_build.md
O primeiro build falhou na fase de bundling devido ao uso de tags Web (`div`) e propriedades incompatíveis (`className`) em componentes nativos.

--- 
### 📄 mobile_37_printer_homologation.md
Com o aplicativo rodando em modo nativo (Missão 36), é necessário validar a integração com hardware real. Esta missão implementa uma interface de diagnóstico para testar a comunicação Bluetooth e a fidelidade dos comandos ESC/POS gerados pelo sistema.

--- 
### 📄 mobile_38_sentry_integration.md
Implementação da camada de telemetria para captura de erros em produção. O objetivo é garantir que falhas silenciosas (crashes nativos ou exceções JS não tratadas) sejam reportadas para a equipe de engenharia.

--- 
### 📄 mobile_hardening_ux.md
Implementar a camada de tratamento visual de erros sistêmicos para garantir que o aplicativo nunca fique em estado indefinido (tela branca ou loading infinito).

--- 

## 📂 Diretorio: `docs/mobile`

### 📄 TEST_PLAN_L6.md
Este plano define os 20 cenários de teste obrigatórios para certificação de loja e estabilidade operacional.

--- 
### 📄 TEST_PLAN_MANUAL.md
Documentação técnica de suporte ao módulo.

--- 

## 📂 Diretorio: `docs/mobile/testing`

### 📄 HUMAN_UI_TEST_MATRIX.md
| ID | Nome | Ação Humana Simulada | Critério de Sucesso | |:---|:---|:---|:---|

--- 
### 📄 HUMAN_UI_TESTS_L5.md
| ID | Nome | Ação Humana Simulada | Critério de Sucesso | |:---|:---|:---|:---|

--- 

## 📂 Diretorio: `docs`

### 📄 NEXT_STEPS.md
Após a auditoria do Omni-Check, as seguintes ações são prioritárias para eliminar o retrabalho: 1. **Executar Omni-Check v1.1:** Rodar `python scripts/validation/omni_check.py` para validar os patches de Unicode.

--- 
### 📄 OFFLINE_ARCHITECTURE_SPEC.md
Utilizamos o **Dexie.js** como wrapper sobre o IndexedDB do navegador. O banco local é chamado `MesaFlowDB`.

--- 

## 📂 Diretorio: `docs/performance`

### 📄 CAPACITY_PLANNING.md
| Métrica | Alvo (Target) | Limite (Threshold) | Ação no Limite | | :--- | :---: | :---: | :--- |

--- 

## 📂 Diretorio: `docs`

### 📄 PITCH.md
Em restaurantes, estádios e hotéis, o maior gargalo é a **fricção no atendimento**:

--- 
### 📄 PLAYBOOK_SUPORTE.md
Guia de diagnóstico para administradores do sistema e suporte técnico.

--- 
### 📄 PRE_PRODUCTION_CHECKLIST.md
Este documento define as condições **obrigatórias** para que o sistema seja movido para o ambiente de produção real. Ignorar qualquer item resultará em veto imediato.

--- 
### 📄 PRO_CHECKLIST.md
Este documento registra os requisitos críticos para a transição do MVP para a fase Comercial (Produção).

--- 
### 📄 PROJECT_OVERVIEW.md
O **MesaFlow** é uma plataforma SaaS (*Software as a Service*) Fullstack desenvolvida para modernizar a operação de food service de ponta a ponta. Mais do que um cardápio digital, ele é um ecossistema que centraliza a operação em uma única nuvem, conectando o salão, a cozinha, o delivery e o back-office em tempo real. O grande diferencial do MesaFlow é sua **Arquitetura Híbrida**: ele permite que o autoatendimento (via QR Code) e o atendimento tradicional (via Garçom) coexistam na mesma comanda, garantindo agilidade sem perder a hospitalidade.

--- 

## 📂 Diretorio: `docs/quality`

### 📄 GOVERNANCE_METRICS.md
Este documento define os indicadores (KPIs) para medir a eficácia da governança técnica do MesaFlow.

--- 

## 📂 Diretorio: `docs/releases`

### 📄 FINAL_RELEASE_v1.0.md
Este release marca a conclusão do plano de aceleração de 72 horas. O sistema evoluiu de um protótipo instável para uma plataforma governada, segura e auditável.

--- 
### 📄 GOLD_MASTER_REPORT.md
O sistema MesaFlow OS completou seu ciclo de endurecimento (Hardening) e está tecnicamente pronto para operação em alta escala. | Domínio | Status | Evidência |

--- 
### 📄 RELEASE_CANDIDATE_1.1.md
| Component | Route | Interactive | Status | |-----------|-------|-------------|--------|

--- 
### 📄 RELEASE_NOTE_v5.1_EXECUTIVO.md
O sistema de automação de qualidade **MesaFlow Optimus** atingiu o nível de maturidade **Enterprise Compliance**. O software está aprovado para uso em ambientes de produção e auditoria contínua.

--- 

## 📂 Diretorio: `docs/reports`

### 📄 ENUM_DRIFT_REPORT.md
✨ Nenhum drift detectado. Todos os dados em produção estão em conformidade com a RFC-009.

--- 
### 📄 FISCAL_PRODUCTION_GO_LIVE.md
Este documento registra a primeira emissão de documento fiscal com valor jurídico real realizada pelo sistema MesaFlow.

--- 

## 📂 Diretorio: `docs/reports/incidents`

### 📄 INCIDENT_TOAST_RACE_CONDITION.md
A análise dos logs de execução do Playwright revela uma **Condição de Corrida Temporal** entre a duração da notificação (Toast) e o tempo de execução da asserção anterior.

--- 

## 📂 Diretorio: `docs/reports`

### 📄 RESILIENCE_STRATEGY_2026.md
O isolamento não é mais lógico (Python), mas físico (PostgreSQL Engine).

--- 
### 📄 ULTIMATE_UI_REPORT.md
Gravação completa disponível em: `docs/reports/videos`

--- 

## 📂 Diretorio: `docs`

### 📄 ROADMAP.md
Este documento é a **fonte única da verdade estratégica** do MesaFlow. Ele não é apenas uma lista de tarefas; é a narrativa da evolução do produto, detalhando as decisões arquiteturais, os desafios de engenharia superados e a visão de futuro que guia nossa expansão.

--- 
### 📄 SCRIPT_INDEX.md
| Script | Tipo | Descrição | | :--- | :---: | :--- |

--- 

## 📂 Diretorio: `docs/sds`

### 📄 ALL_DOCTELAS_CONCAT.md
Esta tela é o núcleo de integridade financeira do MesaFlow OS. Seu objetivo é permitir a conciliação bancária e a auditoria da cadeia de custódia (Ledger L7), garantindo que cada centavo transacionado no gateway (Mercado Pago/Stripe) tenha uma correspondência exata e imutável no banco de dados do sistema.

--- 
### 📄 KIOSK_SYSTEM_SPEC.md
O subsistema Kiosk (Totem) é uma interface de autoatendimento projetada para operar em modo quiosque (fullscreen), com proteções contra saída não autorizada e fluxo de compra simplificado.

--- 

## 📂 Diretorio: `docs/sds/UI_DOCS`

### 📄 EXECUTIVE_UI_SUMMARY.md
| Métrica | Valor | Status | | :--- | :---: | :---: |

--- 
### 📄 FULL_SCREEN_DESCRIPTIONS.md
Este documento detalha a especificação funcional, comportamental e crítica de todas as interfaces do sistema, servindo como referência absoluta para QA, Desenvolvimento e Design.

--- 
### 📄 FULL_UI_REFERENCE.md
Este documento detalha a estrutura, interatividade e fluxos de todas as telas do sistema.

--- 

## 📂 Diretorio: `docs/security`

### 📄 KIOSK_LOCK_PROTOCOL.md
O **Kiosk Lock Mode** é um estado de operação restrito que impede a saída do usuário da aplicação MesaFlow, garantindo a integridade do terminal de autoatendimento.

--- 
### 📄 KIOSK_LOCK_PROTOCOL_V2.md
O sistema opera sob uma FSM estrita gerenciada pelo `KioskContext`:

--- 
### 📄 RLS_COMPLIANCE_HARDENING.md
Para garantir que `set_tenant` foi aplicado, o sistema implementa um **Assert de Sessão** em nível de driver:

--- 
### 📄 RLS_RUNTIME_GOVERNANCE.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 RUNTIME_RLS_GUARD_SPEC.md
Queries que operam fora do RLS (Superuser/Admin) devem utilizar o wrapper `AdminContext`:

--- 
### 📄 SECURITY_POLICY.md
O MesaFlow adota uma abordagem de "Security by Design" e "Defense in Depth". Esta política define as diretrizes de governança, resposta a incidentes e ciclo de vida de desenvolvimento seguro (SDLC).

--- 

## 📂 Diretorio: `docs/specs`

### 📄 CASHBACK_GLOBAL_NETWORK.md
O **MesaFlow Passport** é o módulo B2B2C que unifica a experiência do cliente final em toda a rede de estabelecimentos que utilizam o ecossistema MesaFlow. O objetivo é criar um efeito de rede onde o cashback acumulado em um local possa ser resgatado em qualquer outro parceiro da plataforma.

--- 
### 📄 DASHBOARD_BEHAVIOR.md
Este documento descreve o comportamento esperado, dados exibidos e ações disponíveis em cada tela do Painel Administrativo (`/admin/[slug]/...`).

--- 
### 📄 DRIVER_SCREEN_SPEC.md
Interface simplificada para smartphones, focada em navegação e confirmação de entrega.

--- 
### 📄 FEATURE_FLAGS_UI.md
A interface de Feature Flags é uma ferramenta de nível operacional crítico, destinada exclusivamente à equipe de suporte técnico do MesaFlow. Ela permite a ativação de recursos experimentais (Canary Releases) ou módulos específicos por cliente (Tenant) em tempo real.

--- 
### 📄 FISCAL_HOMOLOGATION.md
Este documento define o protocolo de transição do módulo fiscal do MesaFlow do estado de simulação (Mock) para a operação real com valor jurídico perante a SEFAZ.

--- 
### 📄 FISCAL_PRODUCTION_CHECKLIST.md
Este documento deve ser validado integralmente antes de ativar `FISCAL_ENV=production`.

--- 
### 📄 GUIA_TOKEN_ACESSO.md
O **Token de Acesso** é um código de segurança de 10 dígitos gerado automaticamente pelo MesaFlow sempre que uma mesa é aberta. Ele serve como a "chave mestra" para que o cliente ou o staff recupere uma sessão de pedido ativa.

--- 
### 📄 INFRA_CHECKLIST.md
Para garantir que o ambiente de produção no Render.com esteja otimizado, valide os seguintes pontos baseados nas configurações atuais:

--- 
### 📄 KIOSK_MASTER_REFERENCE.md
Este documento consolida a especificação visual, comportamental e de qualidade para o módulo de Autoatendimento (Totem), integrando `KIOSK_VISUAL_CHECKLIST.md`, `KioskPage.md`, `PUBLIC_KIOSK_OFFLINE.md` e `TASK-FEAT-01`.

--- 
### 📄 KIOSK_QA_CHECKLIST.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 KIOSK_VISUAL_CHECKLIST.md
Este documento consolida a documentação técnica e define o checklist visual rigoroso para a homologação dos Totens de Autoatendimento MesaFlow.

--- 
### 📄 KITCHEN_SCREEN_SPEC.md
Interface de alta visibilidade para tablets, focada em organizar a fila de produção e garantir o cumprimento do SLA.

--- 
### 📄 MANAGER_SCREEN_SPEC.md
Interface Desktop (Next.js) para gestão estratégica, financeira e configuração do tenant.

--- 
### 📄 MODULE_GUIDE.md
Este documento detalha o propósito e as ações disponíveis em cada aba do sistema para garantir a consistência operacional.

--- 
### 📄 PUBLIC_KIOSK_OFFLINE.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 WAITER_APP_V2.md
Ao abrir uma mesa, o garçom deve ser capaz de identificar o cliente para personalizar o atendimento.

--- 
### 📄 WAITER_SCREEN_SPEC.md
Interface nativa (React Native) focada em agilidade de salão. O garçom deve conseguir realizar operações críticas com o mínimo de toques possível.

--- 

## 📂 Diretorio: `docs/sre`

### 📄 FMEA_L10_RESIDUAL_RISK.md
| Modo de Falha | Causa Raiz | Impacto | Mitigação Autônoma L10.2 | | :--- | :--- | :--- | :--- |

--- 
### 📄 RUNBOOK_DISASTER_RECOVERY.md
Este documento descreve os procedimentos técnicos para recuperação de falhas catastróficas e manutenção de segurança.

--- 
### 📄 RUNBOOKS.md
1. Verifique o status em `neon.tech/status`. 2. Se a região estiver offline, acione o script de failover para réplica de leitura (se disponível).

--- 
### 📄 SELF_HEALING_TRIGGERS.md
| Métrica Crítica (Sentry/Prometheus) | Threshold | Ação Automática | | :--- | :--- | :--- |

--- 

## 📂 Diretorio: `docs`

### 📄 SRE_MAINTENANCE_RUNBOOK.md
1.  Verifique o status no painel do Upstash/Render. 2.  O MesaFlow possui fallback automático para memória local. Se o Redis cair, reinicie a API para que ela entre em modo `bypass`.

--- 
### 📄 STABILIZATION_PLAN.md
Fica estabelecido que nenhum código será considerado "Done" sem passar pelo **MesaFlow Omni-Check**. Este é um script mestre (`scripts/validation/omni_check.py`) que dispara simultaneamente:

--- 

## 📂 Diretorio: `docs/strategy`

### 📄 GTM_TACTICAL_GUIDE.md
Este documento expande o `WAR_PLAN_GTM.md` com instruções técnicas e táticas detalhadas para cada frente de batalha.

--- 
### 📄 WAR_PLAN_GTM.md
Esta é uma análise crítica e um **Plano de Guerra** para transformar o código do MesaFlow em um negócio SaaS rentável e escalável. Não basta o código rodar; a operação precisa parar de pé.

--- 

## 📂 Diretorio: `docs/support`

### 📄 TROUBLESHOOTING_N1.md
Este guia é destinado aos atendentes de suporte para resolução rápida de problemas comuns reportados pelos clientes via WhatsApp.

--- 

## 📂 Diretorio: `docs/tasks`

### 📄 TASK-DOC-02.md
Transformar o inventário técnico JSON (gerado na TASK-QA-06) em documentação legível para humanos (Markdown), servindo como referência para designers, QAs e desenvolvedores.

--- 
### 📄 TASK-QA-06.md
Criar um mecanismo automatizado para mapear todas as telas, elementos interativos e fluxos da aplicação Web e Mobile, gerando uma documentação viva do estado atual da interface.

--- 

## 📂 Diretorio: `docs`

### 📄 TASKS.md
Documentação técnica de suporte ao módulo.

--- 

## 📂 Diretorio: `docs/team`

### 📄 INTERVIEW_QUESTIONNAIRE.md
Este questionário visa validar a profundidade técnica e o alinhamento cultural dos candidatos com o Protocolo INDA e a stack do MesaFlow.

--- 

## 📂 Diretorio: `docs/team/questionnaires`

### 📄 architect_100_questions.md
1. O que significa a sigla INDA? 2. Qual a diferença entre a fase de 'Inspection' e 'Normalization'?

--- 
### 📄 backend_100_questions.md
1. Por que o MesaFlow utiliza `async def` em vez de `def` nos endpoints? 2. Como funciona a Injeção de Dependência no FastAPI para o `get_db`?

--- 
### 📄 dev_backend_100_questions.md
1. Como o `asyncio` gerencia o loop de eventos comparado ao threading? 2. Explique a implementação de RLS no PostgreSQL e como o `current_setting` protege o dado.

--- 
### 📄 devops_sre_100_questions.md
1. Por que o MesaFlow utiliza o Render.com para o Web Service e a Vercel para o Frontend? 2. Como o Neon.tech (PostgreSQL Serverless) lida com picos de tráfego repentinos?

--- 
### 📄 frontend_100_questions.md
1. Qual a diferença fundamental entre Server Components e Client Components no MesaFlow? 2. Por que utilizamos o diretório `src/app` em vez do `pages` legado?

--- 
### 📄 frontend_mobile_100_questions.md
1. Qual a diferença entre Server Components e Client Components na hidratação? 2. Como o Zustand gerencia o estado sem causar re-renders globais como o Context API?

--- 
### 📄 mobile_100_questions.md
1. Qual a principal vantagem do Expo Managed Workflow para o MesaFlow? 2. O que é a "New Architecture" (Fabric/TurboModules) e como ela impacta o app?

--- 
### 📄 product_management_100_questions.md
1. Como priorizar o backlog usando o framework RICE em um ambiente de hipercrescimento? 2. Defina a métrica North Star para o MesaFlow OS.

--- 
### 📄 product_manager_100_questions.md
1. Qual a proposta de valor central do MesaFlow OS para um restaurante de alto tráfego? 2. Como o Roadmap é priorizado entre "Dívida Técnica" e "Novas Features"?

--- 
### 📄 qa_100_questions.md
1. Explique a pirâmide de testes aplicada ao ecossistema MesaFlow. 2. O que é o "Omni-Check" e por que ele é a prioridade zero contra o retrabalho?

--- 
### 📄 security_100_questions.md
1. Como mitigar ataques de personificação de tenant em sistemas multi-tenant? 2. Explique o funcionamento do HMAC na validação de webhooks.

--- 

## 📂 Diretorio: `docs/team/roles`

### 📄 ARCHITECT.md
Ser o guardião da **Constituição Técnica** e do **Protocolo INDA**. Este profissional não apenas desenha a solução, mas mantém os scripts de governança (`atualizar.py`, `gerartxt.py`) que permitem que o time (humanos e IAs) trabalhe sem quebrar o sistema.

--- 
### 📄 BACKEND_ENGINEER.md
Construir e manter o motor transacional do MesaFlow, garantindo que nenhuma regra de negócio seja violada e que o isolamento de dados (Multi-tenant) seja absoluto.

--- 
### 📄 DEVOPS_SRE.md
Garantir que o código saia da máquina do desenvolvedor e chegue à produção com segurança, escalabilidade e observabilidade.

--- 
### 📄 FRONTEND_ENGINEER.md
Criar interfaces web rápidas, responsivas e acessíveis para o Painel Administrativo e o Cardápio Digital (PWA).

--- 
### 📄 MOBILE_ENGINEER.md
Desenvolver o "Super App" operacional usado por Garçons, Cozinheiros e Entregadores. O foco é performance, estabilidade e funcionamento **Offline-First**.

--- 
### 📄 PRODUCT_MANAGER.md
Traduzir as necessidades do mercado em especificações técnicas claras, garantindo que o time de engenharia construa o produto certo, na hora certa.

--- 
### 📄 QA_AUTOMATION.md
Criar redes de segurança automatizadas que impeçam regressões. Se o Kernel é a lei, o QA é a auditoria.

--- 

## 📂 Diretorio: `docs/team`

### 📄 ROLES_AND_SKILLS.md
Este documento define a estrutura organizacional necessária para operar o MesaFlow. Ele serve como guia de contratação e como mapa de responsabilidades para os Agentes de IA.

--- 

## 📂 Diretorio: `docs`

### 📄 TECH_DEBT.md
Documentação técnica de suporte ao módulo.

--- 

## 📂 Diretorio: `docs/technical`

### 📄 AI_KNOWLEDGE_BASE.md
` no arquivo de entrada e anexa o conteúdo automaticamente ao arquivo central de conhecimento, garantindo que o aprendizado técnico seja persistido entre as sessões. <Schema_Execution>

--- 
### 📄 AI_KNOWLEDGE_PROTOCOL.md
A base de conhecimento operacional que eu (IA) utilizo para entender o projeto MesaFlow OS está no arquivo:

--- 
### 📄 API_REFERENCE.md
Esta documentação detalha os contratos de integração com a API do MesaFlow, consolidando endpoints públicos, administrativos e de integração.

--- 
### 📄 ASYNC_TASK_LIFECYCLE.md
graph TD O[Order Created] --> T1[dispatch_webhook_task]

--- 
### 📄 BACKEND_SDS.md
1. Request chega com `company_slug`. 2. Middleware resolve `company_id`.

--- 
### 📄 CELERY_HARDENING_STRATEGY.md
Em cenários de falha massiva do provedor (ex: Mercado Pago fora do ar):

--- 
### 📄 DATABASE_RELATIONSHIPS.md
O MesaFlow utiliza um modelo relacional estrito para garantir integridade de dados em um ambiente multi-tenant.

--- 
### 📄 DATABASE_SCHEMA.md
O MesaFlow utiliza PostgreSQL com isolamento lógico por estabelecimento.

--- 
### 📄 DIAGNOSTIC_REPORT_L6.md
O sistema apresenta uma falha estrutural na gestão de estado do Frontend, resultando em um **Loop Infinito de Renderização** (`Maximum update depth exceeded`) que causa o crash silencioso do componente `DriverPage` durante a execução de testes automatizados. A causa raiz não é um "bug simples", mas um **conflito de autoridade de estado**: o Frontend tenta derivar o estado "Ativo" a partir de dados do Backend (via Polling/WebSocket) enquanto simultaneamente tenta impor um estado "Otimista" localmente. Quando esses dois fluxos colidem (especialmente sob a latência de rede simulada ou real), o React entra em ciclo de re-renderização.

--- 
### 📄 ENV_REFERENCE.md
Este documento descreve todas as variáveis de configuração suportadas pelo MesaFlow.

--- 
### 📄 FAILURE_MODES_ANALYSIS.md
| Componente | Modo de Falha | Impacto | Mitigação / Fallback | Runbook | | :--- | :--- | :--- | :--- | :--- |

--- 
### 📄 FLOW_DIAGRAMS.md
Este documento centraliza a lógica visual dos processos críticos do MesaFlow OS.

--- 
### 📄 FMEA_ADVANCED_MODES.md
| Modo de Falha | Causa Raiz | Impacto | Mitigação L10 | | :--- | :--- | :--- | :--- |

--- 
### 📄 FMEA_TRANSACTIONAL_FLOWS.md
| Fluxo | Modo de Falha | Impacto | Mitigação (L8/L9) | Mecanismo de Rollback | | :--- | :--- | :--- | :--- | :--- |

--- 
### 📄 FRONTEND_SDS.md
O `useOfflineSync` monitora a conectividade. Pedidos feitos sem rede são salvos no Dexie e sincronizados automaticamente via `background-sync` assim que o sinal é restaurado.

--- 
### 📄 LEDGER_AUDIT_PROTOCOL.md
O `ReconciliationService` executa às 03:00 UTC: 1. **Fetch:** Coleta transações do Mercado Pago/Stripe das últimas 24h.

--- 
### 📄 LEDGER_RECONCILIATION_V2.md
| Indicador | Threshold | Ação Automática | | :--- | :--- | :--- |

--- 
### 📄 LEDGER_ZERO_DIVERGENCE_PROTOCOL.md
| Cenário de Divergência | Causa Raiz | Threshold Proativo (L10.2) | | :--- | :--- | :--- |

--- 
### 📄 MOBILE_SDS.md
Utiliza a `useAuthStore` (Zustand) com persistência no `Expo SecureStore` para garantir que a sessão sobreviva ao fechamento do app. O `isHydrated` bloqueia a UI até que os tokens sejam validados.

--- 
### 📄 OFFLINE_CONSISTENCY_MATRIX.md
| Cenário | Risco | Mitigação L10 | | :--- | :--- | :--- |

--- 
### 📄 PAGE_DICTIONARY.md
| Rota | Nome | Intenção de Negócio | Comportamento Esperado | | :--- | :--- | :--- | :--- |

--- 

## 📂 Diretorio: `docs/technical/pages`

### 📄 ADMIN_AUDIT_SYSTEM.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_AUTH_RECOVERY.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_COUNTER_POS.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_DASHBOARD.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_DASHBOARD_HISTORY.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_EXPEDITOR.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_FINANCE_AUDIT.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_FINANCE_MARKETING.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_FISCAL_INTEGRATION.md
O sistema utiliza um modelo assíncrono para não bloquear a finalização do pedido. 1.  **Gatilho:** Pedido marcado como `PAID`.

--- 
### 📄 ADMIN_FRANCHISE.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_GENERAL_SETTINGS.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_HISTORY.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_INVENTORY.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_LOGIN.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_LOGISTICS_DELIVERY.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_MARKETING.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_MENU_MANAGEMENT.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_PROFILE.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_SETTINGS_BILLING.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_SETTINGS_FEATURES.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_SUPPORT_PAYMENT.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_TABLES.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_TEAM.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_TEAM_PROFILE.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 ADMIN_WAITER_POS_VARIANTS.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 AUTH_FLOW.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 KITCHEN_MONITOR.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 MOBILE_AUTH_KDS.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 MOBILE_LOGISTICS_TOOLS.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 MOBILE_WAITER_POS.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 PUBLIC_KIOSK_OFFLINE.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 PUBLIC_MENU.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 TRUST_CENTER.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 WAITER_DRIVER_OPERATIONS.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 WAITER_ORDERS_HISTORY.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 WAITER_POS.md
Documentação técnica de suporte ao módulo.

--- 

## 📂 Diretorio: `docs/technical`

### 📄 PERSISTENCE_SYNC_STRATEGY.md
| Store / DB | Tecnologia | Escopo | Risco de Inconsistência | | :--- | :--- | :--- | :--- |

--- 
### 📄 PRD.md
O MesaFlow é uma plataforma SaaS B2B Enterprise projetada para orquestrar operações em ambientes de alto tráfego (Restaurantes, Hotéis, Estádios e Eventos).

--- 
### 📄 PRODUCTION_CHECKLIST_EXPLAINED.md
Este documento explica a racionalidade técnica por trás de cada item do `PRE_PRODUCTION_CHECKLIST.md`. O objetivo é garantir que o SRE ou o Arquiteto entenda *por que* um item é bloqueante.

--- 
### 📄 PROJECT_STRUCTURE.md
Guia de navegação para desenvolvedores e IAs.

--- 
### 📄 SCRIPT_INVENTORY.md
Este inventário cataloga a localização física e funcional de todos os scripts operacionais do sistema, seguindo a estrutura de domínios isolados e a hierarquia suprema do SSOT.

--- 
### 📄 SDS.md
O sistema é composto por um Backend central (API Gateway + Business Logic), múltiplos Frontends (Web Admin, PWA Cliente) e um App Mobile Nativo.

--- 
### 📄 SECURITY_ARCHITECTURE.md
O MesaFlow utiliza **Isolamento Lógico em Nível de Linha (Row-Level Security - RLS)** nativo do PostgreSQL.

--- 
### 📄 SYNC_ARCHITECTURE.md
Todas as interfaces (Site, Admin, App Garçom, KDS, App Driver) conectam-se ao mesmo cluster **PostgreSQL (Neon.tech)**.

--- 
### 📄 TEST_STRATEGY.md
O MesaFlow adota uma estratégia equilibrada para garantir qualidade sem sacrificar velocidade.

--- 
### 📄 TROUBLESHOOTING.md
1.  O Backend não está rodando. 2.  Firewall bloqueando porta 8000.

--- 

## 📂 Diretorio: `docs`

### 📄 TECHNICAL_DEBT_REGISTER.md
Este documento traduz as falhas da auditoria em itens acionáveis de engenharia.

--- 

## 📂 Diretorio: `docs/troubleshooting`

### 📄 TROUBLESHOOTING_MASTER.md
Este documento atua como a **Memória Imunológica** do projeto. Ele registra erros passados, suas causas raízes e a solução definitiva, impedindo a recorrência de falhas conhecidas e acelerando o diagnóstico de incidentes.

--- 

## 📂 Diretorio: `docs/trust`

### 📄 SLA_AVAILABILITY.md
O MesaFlow garante uma disponibilidade mensal de **99,9%** (três noves) para os Serviços Essenciais.

--- 
### 📄 STATUS_PAGE.md
A página de status do MesaFlow é a fonte única da verdade sobre a disponibilidade dos nossos serviços. Ela é hospedada externamente à nossa infraestrutura para garantir comunicação mesmo em caso de falha total do datacenter principal.

--- 

## 📂 Diretorio: `doctelas/_archive/mobile`

### 📄 AppHomescreen.md
Nenhuma interface de props explícita detectada.

--- 
### 📄 AuthLoginscreen.md
Nenhuma interface de props explícita detectada.

--- 
### 📄 CommonLoadingscreen.md
Nenhuma interface de props explícita detectada.

--- 
### 📄 DriverDashboard.md
Gestão de entregas para motoboys próprios.

--- 
### 📄 DriverDriverdashboardScreen.md
// TODO: Listar propriedades detectadas via análise estática interface Props {

--- 
### 📄 DriverScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 HomeScreen.md
Nenhuma interface de props explícita.

--- 
### 📄 KitchenDashboard.md
Nenhuma interface de props explícita.

--- 
### 📄 KitchenKitchendashboardScreen.md
// TODO: Listar propriedades detectadas via análise estática interface Props {

--- 
### 📄 KitchenScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 LoadingScreen.md
Nenhuma interface de props explícita.

--- 
### 📄 LoginScreen.md
Autenticação segura e persistente no dispositivo.

--- 
### 📄 MobileAuthLoginscreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 MobileCommonLoadingscreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 MobileDriverdashboardScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 MobileHomescreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 MobileKitchendashboardScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 MobileOrdersscreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 MobileWaitercallsscreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 MobileWaiterdashboardScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 MobileWaiterOrderentryscreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 MobileWaiterOrderreviewscreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 MobileWaiterPaymentscreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 MobileWaiterPrinterdebugscreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 MobileWaitertablesscreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 OrderEntryScreen.md
Nenhuma interface de props explícita.

--- 
### 📄 OrderReviewScreen.md
Nenhuma interface de props explícita.

--- 
### 📄 OrdersOrdersscreen.md
Nenhuma interface de props explícita detectada.

--- 
### 📄 OrdersScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 PaymentScreen.md
Nenhuma interface de props explícita.

--- 
### 📄 PrinterDebugScreen.md
Diagnóstico de hardware em campo.

--- 
### 📄 SAuthLoginScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 SDriverDriverdashboardScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 SHomeScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 SKitchenKitchendashboardScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 SLoadingScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 SOrdersScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 SWaiterOrderentryScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 SWaiterOrderreviewScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 SWaiterPaymentScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 SWaiterPrinterdebugScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 SWaiterWaitercallsScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 SWaiterWaiterdashboardScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 SWaiterWaitertablesScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 WaiterCallsScreen.md
Nenhuma interface de props explícita.

--- 
### 📄 WaiterDashboard.md
Gestão de salão em movimento.

--- 
### 📄 WaiterOrderentryscreen.md
Nenhuma interface de props explícita detectada.

--- 
### 📄 WaiterOrderreviewscreen.md
Nenhuma interface de props explícita detectada.

--- 
### 📄 WaiterPaymentscreen.md
Nenhuma interface de props explícita detectada.

--- 
### 📄 WaiterPrinterdebugscreen.md
Nenhuma interface de props explícita detectada.

--- 
### 📄 WaiterScreen.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 WaiterTablesScreen.md
Nenhuma interface de props explícita.

--- 
### 📄 WaiterWaitercallsscreen.md
// TODO: Listar propriedades detectadas via análise estática interface Props {

--- 
### 📄 WaiterWaiterdashboardScreen.md
// TODO: Listar propriedades detectadas via análise estática interface Props {

--- 
### 📄 WaiterWaitertablesscreen.md
// TODO: Listar propriedades detectadas via análise estática interface Props {

--- 

## 📂 Diretorio: `doctelas/_archive/web`

### 📄 AdminAuditFinancialPage.md
Nenhuma interface de props explícita detectada.

--- 
### 📄 AdminBillingPage.md
| Elemento | Tipo | Ação | Feedback Visual | Side Effect | | :--- | :--- | :--- | :--- | :--- |

--- 
### 📄 AdminDashboardHistoryPage.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 AdminFeaturesPage.md
| Elemento | Tipo | Ação | Feedback Visual | Side Effect | | :--- | :--- | :--- | :--- | :--- |

--- 
### 📄 AdminFinancialAuditPage.md
// TODO: Listar propriedades detectadas via análise estática interface Props {

--- 
### 📄 AdminForgot-passwordPage.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 AdminForgotpasswordPage.md
Nenhuma interface de props explícita detectada.

--- 
### 📄 AdminReset-passwordPage.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 AdminResetpasswordPage.md
Nenhuma interface de props explícita detectada.

--- 
### 📄 AdminSettingsPage.md
| Elemento | Tipo | Ação | Feedback Visual | Side Effect | | :--- | :--- | :--- | :--- | :--- |

--- 
### 📄 AdminWaiterPos1Page.md
Nenhuma interface de props explícita detectada.

--- 
### 📄 AdminWaiterPosQuickPage.md
Nenhuma interface de props explícita detectada.

--- 
### 📄 DashboardPage.md
| Elemento | Tipo | Ação | Feedback Visual | Side Effect | | :--- | :--- | :--- | :--- | :--- |

--- 
### 📄 KitchenPage.md
| Elemento | Tipo | Ação | Feedback Visual | Side Effect | | :--- | :--- | :--- | :--- | :--- |

--- 
### 📄 LoginPage.md
| Elemento | Tipo | Ação | Feedback Visual | Side Effect | | :--- | :--- | :--- | :--- | :--- |

--- 
### 📄 OrdersPage.md
| Elemento | Tipo | Ação | Feedback Visual | Side Effect | | :--- | :--- | :--- | :--- | :--- |

--- 
### 📄 TrustCenterPage.md
| Elemento | Tipo | Ação | Feedback Visual | Side Effect | | :--- | :--- | :--- | :--- | :--- |

--- 

## 📂 Diretorio: `doctelas/mobile`

### 📄 AuthLoginscreen.md
Porta de entrada única para o staff operacional (Garçons, Cozinha e Motoristas). Garante que apenas usuários autorizados acessem o kernel de operações do restaurante, vinculando o dispositivo ao Tenant correto.

--- 
### 📄 DriverDashboard.md
Gestão de entregas para motoboys próprios.

--- 
### 📄 DriverdashboardScreen.md
Interface principal para o entregador da frota própria. Permite a visualização de pedidos prontos para entrega, gestão de rotas ativas e confirmação de recebimento no destino final, integrando telemetria GPS em tempo real.

--- 
### 📄 HomeScreen.md
Funcionalidade específica do sistema.

--- 
### 📄 KitchenDashboard.md
Funcionalidade específica do sistema.

--- 
### 📄 KitchendashboardScreen.md
Versão nativa do Monitor de Produção, otimizada para tablets instalados em áreas de calor (cozinha) ou balcões de entrega. Sua função é fornecer uma interface de toque robusta para que os cozinheiros gerenciem a fila de produção com zero atrito.

--- 
### 📄 LoadingScreen.md
Funcionalidade específica do sistema.

--- 
### 📄 LoginScreen.md
Autenticação segura e persistente no dispositivo.

--- 
### 📄 OrderEntryScreen.md
Funcionalidade específica do sistema.

--- 
### 📄 OrderReviewScreen.md
Funcionalidade específica do sistema.

--- 
### 📄 OrdersScreen.md
Funcionalidade específica do sistema.

--- 
### 📄 PaymentScreen.md
Funcionalidade específica do sistema.

--- 
### 📄 PrinterDebugScreen.md
Funcionalidade específica do sistema.

--- 
### 📄 WaitercallsScreen.md
Funcionalidade específica do sistema.

--- 
### 📄 WaiterDashboard.md
Gestão de salão em movimento para garçons.

--- 
### 📄 WaiterdashboardScreen.md
O Dashboard do Garçom é o hub inicial de produtividade. Ele fornece uma visão panorâmica das responsabilidades do funcionário no turno, incluindo suas mesas ativas, total de vendas acumuladas e acesso rápido às ferramentas de lançamento e fechamento.

--- 
### 📄 WaiterOrderentryscreen.md
Interface de alta performance para garçons realizarem o lançamento de pedidos na mesa. Focada em velocidade de toque e redução de erros de comunicação com a cozinha.

--- 
### 📄 WaiterOrderreviewScreen.md
Esta tela serve como o "Check-out de Lançamento". É o ponto de revisão final onde o garçom valida os itens selecionados, ajusta quantidades e confirma o envio para a cozinha, garantindo a precisão do pedido antes da produção.

--- 
### 📄 WaiterPaymentScreen.md
Interface de checkout móvel que transforma o smartphone do garçom em um terminal de recebimento. Permite processar pagamentos via Pix (dinâmico), Dinheiro (com calculadora de troco) e Cartão, integrando o fluxo financeiro diretamente ao Ledger do sistema.

--- 
### 📄 WaiterPrinterdebugScreen.md
Ferramenta de diagnóstico e homologação de hardware. Permite que a equipe de suporte e o lojista testem a conectividade Bluetooth e a compatibilidade de comandos ESC/POS com impressoras térmicas locais.

--- 
### 📄 Waitertablesscreen.md
Funcionalidade específica do sistema.

--- 

## 📂 Diretorio: `doctelas`

### 📄 README.md
Esta documentação é gerada de forma híbrida: a estrutura inicial é criada automaticamente pelo script `generate_dynamic_doctelas.py` baseada no código fonte, e os detalhes funcionais são preenchidos por humanos/IA.

--- 

## 📂 Diretorio: `doctelas/web`

### 📄 AdminAuditFinancialPage.md
Esta tela é o núcleo de integridade financeira do MesaFlow OS. Seu objetivo é permitir a conciliação bancária e a auditoria da cadeia de custódia (Ledger L7), garantindo que cada centavo transacionado no gateway (Mercado Pago/Stripe) tenha uma correspondência exata e imutável no banco de dados do sistema.

--- 
### 📄 AdminAuditPage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminBillingPage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminCallbackPage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminCounterPage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminDashboardHistoryPage.md
Esta tela fornece uma trilha de auditoria completa e retroativa de todas as transações e mudanças de estado do sistema. É a ferramenta principal para resolução de disputas financeiras, conferência de fechamento de caixa e análise de performance histórica de longo prazo.

--- 
### 📄 AdminDashboardPage.md
Esta tela é o centro de inteligência tática do MesaFlow OS. Seu objetivo é fornecer ao proprietário e gerentes uma visão consolidada da saúde financeira e operacional do estabelecimento em tempo real, permitindo decisões baseadas em dados sobre estoque, equipe e engenharia de cardápio.

--- 
### 📄 AdminDeliveryPage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminDriverPage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminExpeditorPage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminFeaturesPage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminFinancialPage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminForgotPasswordPage.md
Interface de recuperação de conta para usuários administrativos. Permite que proprietários e funcionários solicitem um link de redefinição de senha via e-mail, garantindo a continuidade do acesso mesmo em caso de perda de credenciais.

--- 
### 📄 AdminFranchisePage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminHistoryPage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminInventoryPage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminKitchenPage.md
O Monitor de Produção (Kitchen Display System - KDS) é a interface crítica para a equipe de preparo. Sua função é substituir as comandas de papel por uma fila digital inteligente, organizada por tempo de permanência e prioridade de SLA.

--- 
### 📄 AdminLoginPage.md
Ponto de acesso centralizado para a administração do ecossistema MesaFlow. Realiza a autenticação de proprietários (Owners) e funcionários (Staff), estabelecendo o contexto de segurança necessário para o isolamento multi-tenant (RLS).

--- 
### 📄 AdminMarketingPage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminMenuPage.md
Funcionalidade específica do sistema.

--- 
### 📄 AdminOrdersPage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminPaymentCallbackPage.md
Esta página atua como o "Handshake Final" entre o MesaFlow e os provedores de pagamento (Mercado Pago/Stripe). Sua função é capturar o código de autorização OAuth, trocá-lo por tokens de acesso e vincular a conta financeira do lojista ao seu Tenant no sistema.

--- 
### 📄 AdminProfilePage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminRegisterPage.md
Portal de auto-cadastro para novos estabelecimentos. O objetivo é permitir que um novo lojista crie sua conta, defina seu subdomínio (slug) e configure os parâmetros básicos do seu negócio em menos de 2 minutos (Zero-Touch Onboarding).

--- 
### 📄 AdminResetPasswordPage.md
Página de destino do link de recuperação de senha. Permite que o usuário defina uma nova credencial de acesso após validar a posse do e-mail através de um token seguro, restaurando o acesso à plataforma administrativa.

--- 
### 📄 AdminSettingsBillingPage.md
Central de faturamento e gestão de planos. Permite ao lojista realizar o upgrade para o plano Pro, gerenciar métodos de pagamento, visualizar faturas passadas e controlar o consumo de recursos do SaaS.

--- 
### 📄 AdminSettingsFeaturesPage.md
Painel de controle de funcionalidades experimentais (Feature Flags). Destinado à equipe de suporte e desenvolvedores (Modo Impersonation), permite ativar ou desativar módulos Beta para clientes específicos sem a necessidade de novo deploy de código.

--- 
### 📄 AdminSettingsPage.md
Central de configuração da identidade e regras de operação do estabelecimento. Permite personalizar a aparência do cardápio, horários de funcionamento, taxas de serviço e integrações de comunicação (WhatsApp).

--- 
### 📄 AdminSupportPage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminTablesPage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminTeamPage.md
Nenhuma interface de props explícita.

--- 
### 📄 AdminWaiterOrdersPage.md
Esta tela é o "Live Feed" de operações do salão. Seu objetivo é permitir que supervisores de garçons e gerentes de turno monitorem o fluxo de pedidos em tempo real, identifiquem gargalos de atendimento e realizem intervenções rápidas em comandas específicas sem a necessidade de estar fisicamente na mesa.

--- 
### 📄 AdminWaiterPage.md
Dashboard administrativo para gestão de capital humano e performance de campo. Permite ao proprietário monitorar a eficiência da equipe de garçons, gerenciar escalas de acesso e auditar a distribuição de gorjetas e comissões.

--- 
### 📄 AdminWaiterPosPage.md
Interface de Ponto de Venda (PDV) otimizada para desktops e tablets. Permite que o staff realize o atendimento completo de uma mesa ou balcão, desde a abertura da comanda até o processamento de pagamentos complexos (divisão de conta).

--- 
### 📄 AuditPage.md
Funcionalidade específica do sistema.

--- 
### 📄 BillingPage.md
Configurações do sistema.

--- 
### 📄 CheckoutPage.md
Funcionalidade específica do sistema.

--- 
### 📄 ClientMenuPage.md
Nenhuma interface de props explícita.

--- 
### 📄 CounterPage.md
Ponto de venda (PDV) para operação de caixa rápida.

--- 
### 📄 DashboardPage.md
Visão tática da operação. Decisões baseadas em dados em tempo real.

--- 
### 📄 DeliveryPage.md
Funcionalidade específica do sistema.

--- 
### 📄 DriverPage.md
Funcionalidade específica do sistema.

--- 
### 📄 ExpeditorPage.md
Funcionalidade específica do sistema.

--- 
### 📄 FeaturesBetaPage.md
Configurações do sistema.

--- 
### 📄 FinancialAuditPage.md
Funcionalidade específica do sistema.

--- 
### 📄 ForgotPasswordPage.md
Funcionalidade específica do sistema.

--- 
### 📄 FranchisePage.md
Funcionalidade específica do sistema.

--- 
### 📄 HistoryPage.md
Funcionalidade específica do sistema.

--- 
### 📄 InventoryPage.md
Funcionalidade específica do sistema.

--- 
### 📄 KioskAttractScreen.md
Funcionalidade específica do sistema.

--- 
### 📄 KitchenPage.md
Orquestração de produção (KDS). Substitui impressoras de cozinha.

--- 
### 📄 LandingPage.md
Porta de entrada comercial. Converte visitantes em leads ou contas de teste (PLG).

--- 
### 📄 LoginPage.md
Autenticação de usuário.

--- 
### 📄 MarketingPage.md
Funcionalidade específica do sistema.

--- 
### 📄 OfflinePage.md
Funcionalidade específica do sistema.

--- 
### 📄 Page.md
Funcionalidade específica do sistema.

--- 
### 📄 PaymentCallbackPage.md
Funcionalidade específica do sistema.

--- 
### 📄 ProfilePage.md
Funcionalidade específica do sistema.

--- 
### 📄 PublicMonitorPage.md
Funcionalidade específica do sistema.

--- 
### 📄 QuickPosPage.md
Funcionalidade específica do sistema.

--- 
### 📄 RegisterPage.md
Cadastro de novos usuários/tenants.

--- 
### 📄 ResetPasswordPage.md
Funcionalidade específica do sistema.

--- 
### 📄 SecurityPage.md
Funcionalidade específica do sistema.

--- 
### 📄 SettingsPage.md
Configurações do sistema.

--- 
### 📄 StatusPage.md
Funcionalidade específica do sistema.

--- 
### 📄 SupportPage.md
Funcionalidade específica do sistema.

--- 
### 📄 TablesPage.md
Funcionalidade específica do sistema.

--- 
### 📄 TeamPage.md
Funcionalidade específica do sistema.

--- 
### 📄 TrustCenterPage.md
Funcionalidade específica do sistema.

--- 
### 📄 TrustSecurityPage.md
Detalhamento técnico das camadas de defesa do sistema. Destinado a CTOs e auditores de segurança, este documento prova como o MesaFlow protege os dados sensíveis e garante o isolamento entre empresas.

--- 
### 📄 TrustStatusPage.md
Monitor de saúde do sistema em tempo real. Fornece aos lojistas e desenvolvedores a confirmação visual de que todos os subsistemas (API, Banco, Real-time) estão operacionais, reduzindo chamados de suporte durante instabilidades globais.

--- 
### 📄 WaiterOrdersPage.md
Funcionalidade específica do sistema.

--- 
### 📄 WaiterPosPage.md
Funcionalidade específica do sistema.

--- 
### 📄 WaiterTablesPage.md
Funcionalidade específica do sistema.

--- 

## 📂 Diretorio: `frontend`

### 📄 README.md
]]></Content> </File>

--- 

## 📂 Diretorio: `governance/evidence`

### 📄 AUDIT_ENV_REPORT.md
These keys are present but have no value set:

--- 
### 📄 BOOTSTRAP_SYNC_REPORT.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 FINAL_L6_RESTRUCTURING_REPORT.md
A estrutura de governança do MesaFlow OS foi elevada ao padrão **Enterprise Gold**. A fragmentação documental foi eliminada e a soberania da pasta `/governance` na raiz está consolidada.

--- 
### 📄 FINAL_RELEASE_REPORT.md
O sistema atingiu a maturidade máxima do Ciclo 3. Todas as barreiras de segurança, integridade e UX foram superadas.

--- 
### 📄 FIX_UNICODE_APPLIED.md
Aplicado patch de compatibilidade Windows (`sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')`) nos scripts críticos de validação.

--- 
### 📄 FULL_TEST_SUITE_REPORT.md
| Teste | Status | Duração | | :--- | :---: | :--- |

--- 
### 📄 GAP_ANALYSIS_REPORT.md
O pipeline de prontidão (`master_readiness_check.py`) avançou após a correção do `audit_env.py`, mas falhou no próximo gate crítico: **RLS (Row-Level Security)**.

--- 
### 📄 GOLD_MASTER_RCA_REMEDIATION.md
O código de despacho foi refatorado para ser **Indulgent-Idempotent**. Se o motorista logado solicitar o despacho de um pedido que ele mesmo já possui, o sistema confirma o sucesso, permitindo que a UI se recupere sem erros.

--- 
### 📄 GOVERNANCE_DEBT_LOG.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 GOVERNANCE_METRICS.md
Este documento define os indicadores (KPIs) para medir a eficácia da governança técnica do MesaFlow.

--- 
### 📄 GOVERNANCE_MIGRATION_L6_REPORT.md
O sistema foi elevado ao nível **Audit-Ready**. A separação entre documentação de produto e governança operacional permite uma triagem técnica 80% mais rápida por auditores externos.

--- 
### 📄 INCIDENT_ENCODING_FIX.md
O sistema falhou ao iniciar a conexão com o banco de dados e ao processar o loop do iFood devido a um erro de decodificação de caracteres no Windows. O byte `0xe7` (caractere `ç`) estava presente em variáveis de ambiente ou no arquivo `.env`, causando o crash do driver `psycopg2`.

--- 
### 📄 INCIDENT_MOCK_DNS_RESOLUTION.md
Ao tentar iniciar o sistema com o `.env` gerado para auditoria, o backend falhou ao resolver o endereço `aws.neon.tech`.

--- 
### 📄 INCIDENT_REPORT_ENCODING.md
O script `systemic_truth_engine.py` sofreu um crash fatal durante a fase de meta-auditoria ao tentar ler arquivos de script que continham caracteres UTF-8 não suportados pelo encoding padrão do Windows (`cp1252`).

--- 
### 📄 INCIDENT_REPORT_GOLD_MASTER.md
O log do sistema indica: `⚠️ Redis Cache indisponível: Timeout connecting to server`. No MesaFlow, o `WebSocketManager` utiliza o Redis Pub/Sub para garantir que, quando um processo de API (Worker A) atualiza um pedido, todos os clientes conectados (Navegadores) recebam a notificação, independentemente de qual Worker de WebSocket eles estejam conectados. Sem o Redis, o broadcast fica restrito à memória local do processo, quebrando a reatividade em ambientes multi-processo (como o modo `reload` do Uvicorn).

--- 
### 📄 INCIDENT_UNICODE_WINDOWS.md
A execução do script de validação mestre (`master_readiness_check.py`) falhou ao invocar o subsistema de integridade (`system_integrity_check.py`). O processo foi abortado devido a uma exceção de codificação de caracteres no ambiente Windows.

--- 
### 📄 INSPECTION_REPORT_L6.md
O sistema encontra-se na transição da **Fase 1 (Infra & Segurança)** para a **Fase 2 (Aplicação)**.

--- 
### 📄 INSPECTION_REPORT_L6_FINAL.md
1.  **Reiniciar API:** Garanta que `python run.py` esteja rodando em um terminal separado. 2.  **Validar Ambiente:** Execute `python scripts/validar/audit_env.py` (SEC-04).

--- 
### 📄 INSPECTION_REPORT_L7_START.md
O MesaFlow OS encontra-se estruturalmente selado. A fundação de **Isolamento de Dados (RLS)** e **Integridade Financeira (Ledger)** é imutável.

--- 
### 📄 INTEGRATION_ROADMAP.md
Este documento mapeia as configurações pendentes para o fechamento do ciclo de produção.

--- 
### 📄 L8_SIMULATION_SPEC.md
A simulação não é mais um script linear. Ela é governada pela classe `StateMachine`, que valida cada transição de status do pedido. Se o backend permitir uma transição ilegal, a automação aborta e reporta a falha de domínio.

--- 
### 📄 MIGRATION_VERIFICATION_REPORT.md
| Table | RLS Enabled | | :--- | :---: |

--- 
### 📄 PIPELINE_CANONICO.md
| ID | Script | Função | Criticidade | Pré-requisito | |:---|:---|:---|:---|:---|

--- 
### 📄 REACT_ARCHITECTURE_REPORT.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 REPORT_APP_01.md
Validar se a camada de persistência consegue injetar o contexto de Tenant na sessão do banco.

--- 
### 📄 REPORT_APP_02.md
Garantir que o serviço de pagamentos bloqueie o re-processamento de IDs externos já existentes.

--- 
### 📄 REPORT_AUDITOR_SIMULATION.md
REGISTRY_PATH = "comunication/registry.xml" REPORT_PATH = "comunication/reports/REPORT_READINESS_SUMMARY.md"

--- 
### 📄 REPORT_AUTOMATION_HARDENING.md
Falha sistemática em testes E2E devido a seletores de interface ambíguos. O uso de `:has-text` causava colisões com múltiplos elementos no DOM, violando o `strict mode` do Playwright.

--- 
### 📄 REPORT_BEHAVIOR_TEST.md
| Cenário | Status | Passos | | :--- | :---: | :--- |

--- 
### 📄 REPORT_BKP_01.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 REPORT_DEEP_INTERACTION.md
| Página | Elemento | Comportamento Esperado | Realidade | Status | | :--- | :--- | :--- | :--- | :---: |

--- 
### 📄 REPORT_DIAG_01.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 REPORT_DOC_PHASE_CONCLUSION.md
A documentação do MesaFlow agora opera em três níveis de abstração: 1.  **Governança (`/governance`):** Leis, Protocolos e Evidências (Imutável/Auditável).

--- 
### 📄 REPORT_DOC_STRUCTURE_V2.md
A estrutura de documentação em `doctelas/` foi auditada e normalizada para eliminar ambiguidades de nomenclatura e duplicidade de arquivos.

--- 
### 📄 REPORT_E2E_SUCCESS.md
O script `e2e_system_flow_v2.py` executou com sucesso o ciclo completo de um pedido, validando a integração entre todas as camadas do sistema.

--- 
### 📄 REPORT_ENUM_DRIFT.md
Foi detectada uma inconsistência estrutural crítica entre o estado atual do `registry.xml` e a Máquina de Estados Canônica definida no Protocolo INDA V10.

--- 
### 📄 REPORT_ENUM_MIGRATION.md
Nenhuma alteração necessária. O arquivo já estava em conformidade.

--- 
### 📄 REPORT_EXHAUSTIVE_INTERACTION.md
| Página | Elemento | Expectativa | Realidade | Status | | :--- | :--- | :--- | :--- | :---: |

--- 
### 📄 REPORT_FINAL_HARDENING.md
Implementado `with_for_update()` no banco de dados para os fluxos de despacho.

--- 
### 📄 REPORT_FINAL_STABILIZATION.md
Implementada regra no backend (`admin_delivery.py`) que impede que um motorista assuma múltiplos pedidos simultaneamente ou que um pedido seja coletado sem estar pronto.

--- 
### 📄 REPORT_FINAL_STATUS_v3.md
O sistema completou **todos** os ciclos de validação crítica. A integridade dos artefatos foi restaurada e a observabilidade está ativa. | Domínio | Status | Detalhes |

--- 
### 📄 REPORT_FULL_COVERAGE.md
| Método | Rota (Path) | Status | Código | | :--- | :--- | :---: | :---: |

--- 
### 📄 REPORT_FULL_SYSTEM_AUDIT.md
| Rota | Status | Botões | Links | Inputs | Erros | | :--- | :---: | :---: | :---: | :---: | :---: |

--- 
### 📄 REPORT_GOLD_MASTER_FINAL.md
O MesaFlow OS completou todos os ciclos de validação do Protocolo INDA L6. Todos os bloqueios impeditivos foram resolvidos ou mitigados.

--- 
### 📄 REPORT_GOLD_MASTER_STATUS.md
| Domínio | Status | Observação | | :--- | :---: | :--- |

--- 
### 📄 REPORT_GOLD_MASTER_V1.md
O "esqueleto" e os "músculos" do sistema estão formados e operacionais. O sistema é capaz de rodar, persistir dados, autenticar usuários e renderizar todas as interfaces sem erros de código. | Camada | Status | Evidência |

--- 
### 📄 REPORT_GOV_01.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 REPORT_GOV_01_XML_PRESENCE.md
| Arquivo | Status | | :--- | :---: |

--- 
### 📄 REPORT_GOV_02.md
| Arquivo | Header Detectado | Status | | :--- | :---: | :---: |

--- 
### 📄 REPORT_GOV_03.md
| Arquivo | Status | Detalhes | | :--- | :---: | :--- |

--- 
### 📄 REPORT_GOV_04.md
All scripts defined in `registry.xml` are present on the disk. The governance structure is consistent.

--- 
### 📄 REPORT_GOV_PROMPT_FIX.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 REPORT_GOVERNANCE_CHANGELOG.md
Este documento substitui o uso da tag `<Governance_Override>` no `registry.xml`, centralizando justificativas de alterações sensíveis conforme Protocolo INDA V10.

--- 
### 📄 REPORT_INCIDENT_RESOLUTION_TOAST.md
A falha intermitente nos testes E2E foi causada por uma **dependência incorreta de elementos efêmeros (Toasts)** para validação de sucesso.

--- 
### 📄 REPORT_INCIDENT_TOAST_RACE_CONDITION.md
A falha intermitente nos testes E2E foi identificada como uma **Condição de Corrida Temporal** entre o tempo de resposta do backend e a asserção do teste, agravada pela falta de feedback visual de carregamento.

--- 
### 📄 REPORT_INF_01.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 REPORT_INF_02.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 REPORT_INF_03.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 REPORT_INF_04.md
{ "node": {

--- 
### 📄 REPORT_MAP_INTEGRATION.md
O sistema de rastreamento foi migrado de uma simulação cinemática (CSS transforms) para uma projeção geográfica real utilizando a biblioteca Leaflet.

--- 
### 📄 REPORT_OBS_01.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 REPORT_OBS_01_DIAG.md
O script executa a seguinte lógica: 1.  Lê a variável de ambiente `SENTRY_DSN_BACKEND`.

--- 
### 📄 REPORT_OMNI_SIMULATION_SUCCESS.md
A simulação de ponta a ponta do módulo de Delivery foi concluída com êxito total. Este teste prova a maturidade da infraestrutura de comunicação em tempo real e a integridade do fluxo transacional.

--- 
### 📄 REPORT_OMNISCIENCE.md
A varredura completa da estrutura `frontend/src/app` identificou **34 rotas ativas**.

--- 
### 📄 REPORT_PHASE_1_CONCLUSION.md
O sistema está autorizado a prosseguir para a validação da lógica de aplicação e integridade de dados.

--- 
### 📄 REPORT_PHASE_2_CLOSURE.md
Os scripts de validação de aplicação foram migrados para um modelo de **Inspeção Passiva**.

--- 
### 📄 REPORT_PHASE_2_START.md
A FASE 1 (Segurança/RLS) foi concluída com sucesso na parte de inventário e matriz de roles. O incidente de permissão no script **SEC-01D** foi endereçado com uma lógica de auto-correção (`GRANT` dinâmico).

--- 
### 📄 REPORT_PHASE_3_READINESS.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 REPORT_PRODUCTION_SEAL.md
O sistema MesaFlow OS passou por todos os testes de estresse, segurança e integridade. A arquitetura multi-tenant está blindada e o motor transacional é determinístico.

--- 
### 📄 REPORT_QA_VISUAL_INSPECTION.md
Com base nos logs de execução fornecidos: | Componente | Status | Porta | Observação |

--- 
### 📄 REPORT_READINESS_SUMMARY.md
O MesaFlow atingiu o nível de maturidade **L5 (Self-Correcting)**. A plataforma é governada por IA e pipelines automatizados.

--- 
### 📄 REPORT_SEC_01.md
| Test Scenario | Result | Evidence | | :--- | :---: | :--- |

--- 
### 📄 REPORT_SEC_01_FAILURE_ANALYSIS.md
1. Criar Role `mesaflow_app` sem privilégios de superuser. 2. Alterar `app/database.py` para garantir que o pool de conexões execute `SET row_security = on`.

--- 
### 📄 REPORT_SEC_01A.md
Este relatório valida se o motor do banco de dados está protegendo as tabelas core. | Tabela | RLS Ativo | Forçado (FORCE) | Status |

--- 
### 📄 REPORT_SEC_01B.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 REPORT_SEC_01C.md
Validação da variável de sessão necessária para o funcionamento do RLS.

--- 
### 📄 REPORT_SEC_01D.md
Este teste prova que o PostgreSQL está injetando o filtro de segurança antes de tocar no disco.

--- 
### 📄 REPORT_SEC_04.md
Ambiente validado e seguro para o nível atual.

--- 
### 📄 REPORT_SEC_05.md
| Header | Status | | :--- | :---: |

--- 
### 📄 REPORT_SENTRY_SETUP.md
Sem o Sentry, o sistema roda "às cegas". Se um erro 500 ocorrer em produção, não haverá log centralizado, stack trace ou contexto do usuário. O Protocolo INDA L6 proíbe deploys sem observabilidade.

--- 
### 📄 REPORT_STABILIZATION_L6.md
Apesar da suíte de testes ter retornado "PASS", a análise profunda dos logs de runtime revelou anomalias que comprometem a integridade do selo **Gold Master**.

--- 
### 📄 REPORT_STRATEGIC_ALIGNMENT.md
Este documento formaliza as respostas às questões cirúrgicas do Auditor Nível 0, definindo a postura do sistema para o Go-Live.

--- 
### 📄 REPORT_SYNTAX_FIX.md
O build do Next.js falhou com `ModuleBuildError` devido a um erro de sintaxe no arquivo `frontend/src/lib/api.ts`.

--- 
### 📄 REPORT_SYSTEM_INTEGRITY.md
| Diretório | Status | | :--- | :---: |

--- 
### 📄 REPORT_SYSTEM_STABLE.md
O incidente crítico de **Rota Inexistente (404)** no endpoint `/api/admin/audit` foi resolvido e verificado. | Teste | Resultado Anterior | Resultado Atual | Evidência |

--- 
### 📄 REPORT_UI_INTERACTIONS.md
| Arquivo | Botões | Links | Inputs | Alertas | | :--- | :---: | :---: | :---: | :--- |

--- 
### 📄 REPORT_ZERO_CONFIG_GAPS.md
O sistema está **90% Zero-Config**. As lacunas restantes são configuracionais externas e inevitáveis em arquiteturas distribuídas.

--- 
### 📄 RLS_CONTEXT_INSPECTION.md
| Table | RLS Enabled | Policies | | :--- | :---: | :--- |

--- 
### 📄 RLS_FAILURE_ANALYSIS.md
O script de validação `verify_TASK-SEC-01.py` falhou, indicando que o **Tenant B** conseguiu ler dados do **Tenant A**.

--- 
### 📄 RLS_FATAL_LEAK_REPORT.md
Durante a execução do script `verify_TASK-SEC-01.py`, o sistema permitiu que um contexto de banco de dados (Tenant B) visualizasse dados privados de outro contexto (Tenant A).

--- 
### 📄 RLS_GUC_REMEDIATION_LOG.md
O script de validação v9 falhou na etapa final devido ao erro `psycopg2.errors.InsufficientPrivilege`. A causa foi a tentativa do papel `mesaflow_app` de executar uma query enquanto o parâmetro global `row_security` estava definido como `off` (herdado da etapa de setup administrativo).

--- 
### 📄 RLS_HARDENING_DIAGNOSTIC.md
O erro `UndefinedColumn: column "company_id" does not exist` revelou que a política de segurança global não pode ser "copy-paste" para todas as tabelas. Algumas tabelas no MesaFlow seguem uma hierarquia relacional onde o isolamento deve ser herdado.

--- 
### 📄 RLS_MIGRATION_REPORT.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 RLS_POLICY_VERIFICATION.md
| Table | RLS Active | Policy Name | Status | | :--- | :---: | :--- | :---: |

--- 
### 📄 RLS_SUPERUSER_BYPASS_WARNING.md
As falhas reportadas no `verify_TASK-SEC-01.py` v8 não foram causadas por erro na lógica do RLS, mas sim pelo uso do usuário `postgres` (Superuser) para realizar os testes.

--- 
### 📄 RLS_VALIDATION_REPORT.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 SCHEMA_DISCOVERY_REPORT.md
This report represents the **single source of truth** of the current database schema.

--- 
### 📄 SECURITY_INCIDENT_RLS_LEAK.md
O script de validação de segurança (`verify_TASK-SEC-01.py`) detectou uma falha crítica no isolamento multi-tenant. Um tenant (B) conseguiu ler dados pertencentes a outro tenant (A) através de uma query padrão do ORM, indicando que o Row-Level Security (RLS) não está ativo ou não está sendo aplicado corretamente.

--- 
### 📄 SECURITY_SEAL_L6.md
O sistema de isolamento **Row-Level Security (RLS)** foi exaustivamente testado e validado sob o protocolo **INDA Strict**.

--- 
### 📄 SIMULATION_FAILURE_ANALYSIS.md
A execução do script `delivery_realtime_simulation.py` falhou com `AssertionError` no passo [3/5]. O Playwright não encontrou o texto "Pronto" na página de acompanhamento do cliente.

--- 
### 📄 SIMULATION_VISIBILITY_FIX.md
A simulação de entrega falhava porque o cliente não conseguia visualizar o status "Pronto". A investigação revelou que o componente `OrderStatusView.tsx` ocultava o rastreamento para pedidos com pagamento pendente.

--- 
### 📄 SQL_MIGRATION_REPORT.md
| File | Status | Message | | :--- | :---: | :--- |

--- 
### 📄 STABILIZATION_REPORT_L6.md
Apesar da suíte de testes ter retornado "PASS", a análise profunda dos logs de runtime revelou anomalias que comprometem a integridade do selo **Gold Master**.

--- 

## 📂 Diretorio: `governance/policies`

### 📄 CHANGE_MANAGEMENT.md
Todas as alterações de código aplicadas por IA ou humanos devem seguir:

--- 
### 📄 DATA_PRIVACY.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 deprecation_policy.md
Define os estados de ciclo de vida: ACTIVE, DEPRECATED, RETIRED.

--- 
### 📄 enum_lifecycle.md
Todas as colunas de status, roles e tipos devem ser String(50) no banco de dados. O código Python deve utilizar enum.Enum para lógica de negócio.

--- 
### 📄 KIOSK_SECURITY_POLICY.md
O modo Kiosk deve atuar como uma sandbox visual. É terminantemente proibido o uso de qualquer lógica de redirecionamento automático para rotas fora do escopo `/[slug]/kiosk` ou `/[slug]/menu` enquanto o estado `LOCKED` ou `BREACHED` estiver ativo.

--- 
### 📄 SECURITY.md
Documentação técnica de suporte ao módulo.

--- 

## 📂 Diretorio: `governance/protocols`

### 📄 ADR_SDS_TRACEABILITY.md
| ADR ID | Decisão Técnica | SDS Relacionado | Task de Implementação | | :--- | :--- | :--- | :--- |

--- 
### 📄 AI_KERNEL_L5_SPEC.md
A IA Kernel L5 não apenas gera código, ela: 1.  **Observa:** Monitora logs, telas e estados em tempo real.

--- 
### 📄 AI_ROLE_PROTOCOL.md
Definir formalmente as fronteiras cognitivas e operacionais de cada instância de Inteligência Artificial no ecossistema MesaFlow. Este documento elimina a ambiguidade de responsabilidades.

--- 
### 📄 AI_SCOPE_VIOLATION_PROTOCOL.md
Definir os critérios para identificar, classificar e remediar violações de escopo por parte das IAs operantes.

--- 
### 📄 AUDIT_TECHNICAL_REPORT.md
O MesaFlow OS opera sob o princípio de **Causalidade Financeira**. O estado do sistema é uma função das transações confirmadas.

--- 
### 📄 CODE_CHANGE_PROTOCOL.md
Padronizar como o código fonte do MesaFlow pode ser alterado, garantindo que toda linha de código tenha uma razão de existir rastreável e que a infraestrutura cognitiva seja preservada.

--- 
### 📄 CONTEXT_GENERATION_PROTOCOL.md
Este protocolo define a estrutura rígida da "Memória de Curto Prazo" da IA. O arquivo `todososarquivos.txt` não é um dump aleatório; é uma **narrativa técnica estruturada** para garantir o alinhamento da personalidade e do contexto. O script `gerartxt.py` é considerado **infraestrutura cognitiva crítica**. Ele é a "retina" da IA. Qualquer erro, ruído excessivo ou omissão indevida neste script causa:

--- 
### 📄 CONTEXT_PRIORITY_PROTOCOL.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 DEFINITION_OF_DONE.md
Este documento define os critérios obrigatórios para que qualquer tarefa seja considerada "Concluída" e elegível para merge na branch de produção.

--- 
### 📄 DOCUMENTATION_STANDARD_PROTOCOL.md
Padronizar a criação e manutenção de documentação para garantir que o conhecimento sobreviva à troca de contexto das IAs.

--- 
### 📄 DOMAIN_VALUES.md
Este documento lista os valores canônicos permitidos para campos enumerados no sistema. Qualquer divergência entre este documento e o código (`app/models/core.py`) é considerada uma violação de integridade.

--- 
### 📄 ERROR_RESPONSE_MAPPING_PROTOCOL.md
Definir o comportamento determinístico que a IA deve adotar ao receber um código de erro do executor `atualizar.py`.

--- 
### 📄 ERROR_TAXONOMY.md
Esta taxonomia padroniza os códigos de erro emitidos pelo Kernel e seus subsistemas.

--- 
### 📄 EXECUTION_ORDER_CYCLE_4.md
Este documento define o caminho crítico e a cronologia de execução para as frentes de trabalho do Ciclo 4, garantindo que as dependências de governança precedam a implementação técnica.

--- 
### 📄 FAIL_FAST_PROTOCOL.md
Abortar imediatamente execuções malformadas para preservar a integridade do sistema MesaFlow e economizar recursos computacionais.

--- 
### 📄 FILE_OWNERSHIP_PROTOCOL.md
Definir a matriz de responsabilidade sobre os arquivos do projeto. Quem pode ler e quem pode escrever em cada diretório.

--- 
### 📄 HANDOVER_PACKAGE.md
1.  **Iniciar Boot:** Ler o `governance_bundle.txt` (gerado por `gerar_kernel.py`). 2.  **Seguir Sequência:** Processar a `AI_STARTUP_SEQUENCE.xml` até o estado `READY`.

--- 
### 📄 HOTFIX_L5_1.md
Um Hotfix L5.1 só é autorizado se:

--- 
### 📄 HOTFIX_MIGRATION_TEMPLATES.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 HYPEROPTIMUS_MASTER_SPEC.md
Este documento é a **Constituição Técnica** do MesaFlow. Ele integra arquitetura, governança e protocolos em um framework unificado e auditável.

--- 
### 📄 IA_L5_TO_L6.md
O sistema agora opera com capacidade de auto-cura e execução de testes complexos sem intervenção humana direta.

--- 
### 📄 INDA_TASK_PROTOCOL.md
O sistema opera em **Kernel Fechado**: A Task é a única fonte de verdade.

--- 
### 📄 KERNEL_INDA_PROTOCOL.md
No contexto do MesaFlow, o **Kernel** não é apenas o núcleo do software, mas a **Entidade Central de Governança**.

--- 
### 📄 L10_AUTONOMOUS_GOVERNANCE.md
Cada execução do `atualizar.py` gera um **Manifesto de Ciclo** em `governance/evidence/cycles/`:

--- 
### 📄 L10_VERSIONING_STANDARDS.md
Toda Task no `TASKS.md` deve conter o link para a ADR correspondente:

--- 
### 📄 L6_AUTONOMOUS_EVOLUTION.md
Até o nível L5, o Kernel atuava como **Guardião** (impedir erros). No nível L6, o Kernel atua como **Evolucionista** (melhorar o que já funciona).

--- 
### 📄 MATURITY_MODELS.md
Este documento define os níveis de maturidade técnica e de governança para os domínios do ecossistema.

--- 
### 📄 MIHP_PROTOCOL.md
Garantir transferência limpa, segura e sem contaminação cognitiva entre diferentes inteligências artificiais dentro do ecossistema MesaFlow. Este protocolo assegura que:

--- 
### 📄 OPTIMUS_v9_Architecture.md
Este documento constitui a especificação técnica definitiva, nível industrial, do sistema **OPTIMUS v9.1**. Ele detalha os algoritmos, fluxos de dados, modelos cognitivos e a infraestrutura de autoaprendizagem que governa a automação de QA do MesaFlow.

--- 
### 📄 PRE_PRODUCTION_CHECKLIST.md
Este documento define as condições **obrigatórias** para que o sistema seja movido para o ambiente de produção real. Ignorar qualquer item resultará em veto imediato.

--- 
### 📄 PROTOCOLS_AND_COMPLIANCE.md
Toda alteração no MesaFlow OS deve seguir: 1. **Inspection:** Auditoria do estado atual via `gerartxt.py`.

--- 
### 📄 ROLLBACK_PROTOCOL.md
Garantir a reversibilidade de qualquer ação executada pelas IAs, protegendo a integridade do projeto contra alucinações, erros de lógica ou corrupção de arquivos.

--- 
### 📄 SECURITY_BOUNDARY_PROTOCOL.md
Definir as fronteiras lógicas de segurança para impedir vazamento de dados, credenciais ou contexto entre ambientes e papéis.

--- 
### 📄 SOS_SYSTEM_STATE.md
Este protocolo define o comportamento do sistema em caso de falha catastrófica ou corrupção de integridade.

--- 
### 📄 TASK_CHECKLIST_TEMPLATE.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 TASK_LIFECYCLE_PROTOCOL.md
Definir os estados possíveis de uma tarefa e os critérios para transição, evitando tarefas "zumbis" ou falsos positivos.

--- 
### 📄 TEMPLATES_AND_STANDARDS.md
Documentação técnica de suporte ao módulo.

--- 
### 📄 TRUTH_HIERARCHY_PROTOCOL.md
Este protocolo define a precedência de evidências em caso de conflito de diagnóstico.

--- 
### 📄 UPDATE_EXECUTION_PROTOCOL.md
Este protocolo define o funcionamento do **MesaFlow Kernel Executor**, um sistema operacional cognitivo que orquestra o **Ciclo INDA** (Input, Neural, Decision, Action). O objetivo é garantir integridade, segurança e durabilidade (ACID) em cada intervenção no código, exigindo que a IA forneça não apenas o código, mas também os comandos para aplicá-lo e validá-lo.

--- 
### 📄 VERIFICATION_PROTOCOL.md
Eliminar a subjetividade na entrega de tarefas. Uma missão só é considerada cumprida se passar por critérios objetivos de verificação automatizada.

--- 

## 📂 Diretorio: `governance`

### 📄 README.md
Este diretório é a **Fonte de Verdade (SSOT)** para o estado de prontidão do sistema.

--- 

## 📂 Diretorio: `governance/rfc`

### 📄 RFC-001.md
O **Context Bundle** (`todososarquivos.txt`) é a representação serializada do estado atual do projeto. Ele é a única entrada sensorial permitida para a IA.

--- 
### 📄 RFC-002.md
O **Kernel Journal** (`kernel_journal.jsonl`) é um log imutável, append-only, que registra todos os eventos de mudança de estado do sistema.

--- 
### 📄 RFC-003.md
Definir a sequência de inicialização do contexto cognitivo da IA.

--- 
### 📄 RFC-004.md
Tarefas geradas automaticamente pelo **Cortex Optimizer** devem seguir um formato estrito para serem reconhecidas pelo Kernel na próxima iteração.

--- 
### 📄 RFC-005.md
Garantir a reversibilidade de qualquer operação de escrita através de backups atômicos.

--- 
### 📄 RFC-006.md
Mecanismo de exceção que permite à IA alterar arquivos protegidos pelo Kernel.

--- 
### 📄 RFC-007.md
Definir os limites operacionais do Kernel para impedir vazamento de dados ou execução de código malicioso.

--- 
### 📄 RFC-008.md
Fica estabelecido que o Enterprise UI Explorer v5.1 constitui a Baseline de Produção Oficial.

--- 
### 📄 RFC-009.md
O uso de Enum nativo causa falhas de migração e erros de runtime.

--- 
### 📄 RFC-010.md
Estabelecer um rito formal para a evolução de tipos enumerados (Enums) no MesaFlow, garantindo que a introdução de novos estados ou a remoção de antigos não cause falhas em clientes (Mobile/Frontend) com versões de cache divergentes.

--- 
### 📄 RFC-011.md
Definir as restrições de hardware e tempo para a execução de modelos de Inteligência Artificial (IA) no MesaFlow, garantindo que o motor preditivo não degrade a performance da API transacional.

--- 
### 📄 RFC-SCRIPT-ORGANIZATION.md
A estrutura de scripts do projeto apresentava redundância e dispersão. Para atingir a maturidade L6, é imperativo que cada ferramenta resida em um domínio funcional único.

--- 

## 📂 Diretorio: `Limpando/comunication/reports`

### 📄 SCHEMA_DISCOVERY_REPORT.md
This report represents the **single source of truth** of the current database schema.

--- 

## 📂 Diretorio: `mobile/.expo`

### 📄 README.md
Documentação técnica de suporte ao módulo.

--- 

## 📂 Diretorio: `mobile`

### 📄 PRODUCTION_LOCK_MOBILE.md
✅ UI Sweep: 11/11 telas renderizadas ✅ Sanity Check: PASS

--- 

## 📂 Diretorio: `.`

### 📄 SECURITY.md
We actively support the security of the following versions of MesaFlow: | Version | Supported          |

--- 
