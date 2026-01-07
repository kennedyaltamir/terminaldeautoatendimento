# 🚩 Especificação Técnica: UI de Gestão de Feature Flags

## 1. Visão Geral
A interface de Feature Flags é uma ferramenta de nível operacional crítico, destinada exclusivamente à equipe de suporte técnico do MesaFlow. Ela permite a ativação de recursos experimentais (Canary Releases) ou módulos específicos por cliente (Tenant) em tempo real.

## 2. Fluxo de Dados

### 2.1 Leitura (Fetch)
- **Gatilho:** Montagem da página ou refresh manual.
- **Endpoint:** `GET /api/admin/features`
- **Contrato:** Retorna um objeto JSON `{ "flag_key": boolean }`.
- **Estado de Loading:** Exibição de Skeletons específicos para a lista de toggles.

### 2.2 Escrita (Mutation)
- **Gatilho:** Alteração do estado do componente `Switch` (Toggle).
- **Endpoint:** `POST /api/admin/features`
- **Payload:** `{ "key": string, "is_enabled": boolean }`
- **Comportamento:** Atualização otimista na UI, seguida de confirmação do backend. Em caso de erro, o estado deve ser revertido imediatamente.

## 3. Protocolo de Segurança (Impersonation)
A UI deve validar a permissão em três camadas:
1.  **Camada de Rota:** O `middleware.ts` ou o `layout.tsx` deve verificar a presença da claim `impersonator: true` no JWT.
2.  **Camada de Contexto:** O `FeatureFlagContext` deve expor o estado `isImpersonator` para esconder/mostrar elementos de edição.
3.  **Camada de API:** O backend já valida o token; a UI deve tratar o erro `403` redirecionando para uma tela de "Acesso Negado".

## 4. Matriz de Estados e Erros

| Cenário | Comportamento da UI | Feedback ao Usuário |
| :--- | :--- | :--- |
| **Usuário Comum** | Bloqueio total da rota `/settings/features`. | "Acesso restrito ao suporte técnico." |
| **Erro de Rede** | Desabilita os toggles temporariamente. | Toast: "Erro de conexão. Tente novamente." |
| **Sucesso no Toggle** | Mantém o novo estado. | Toast: "Funcionalidade [X] atualizada." |
| **Erro 422 (Schema)** | Reverte o toggle para o estado anterior. | Toast: "Falha crítica: Contrato de API violado." |

## 5. Componentização
- `FeatureFlagProvider`: Gerencia o estado global das flags e a verificação de impersonation.
- `FeatureToggleCard`: Componente visual que encapsula o Switch, Label e Descrição da flag.
- `FeaturesPage`: View principal que renderiza a lista de flags disponíveis.

---
*Versão 1.0 - Janeiro de 2026*
