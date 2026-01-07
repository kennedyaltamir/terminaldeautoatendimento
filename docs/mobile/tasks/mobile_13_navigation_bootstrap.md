# 📱 Task 13: Bootstrap de Navegação e Integração de Estado

## 1. Contexto
Materialização do fluxo de navegação do aplicativo, conectando a Store de Autenticação (`useAuthStore`) ao container de navegação nativo. O objetivo é criar um sistema reativo onde a UI transita automaticamente baseada no status da sessão.

## 2. Arquitetura de Roteamento
O `RootNavigator` atua como o orquestrador central, observando o `status` da Store:

- **Status: `hydrating` / `idle`** -> Renderiza `LoadingScreen`.
- **Status: `unauthenticated`** -> Renderiza `AuthStack` (Login).
- **Status: `authenticated`** -> Renderiza `AppStack` (Home/Operacional).

## 3. Decisões Arquiteturais Explícitas
- **Equivalência `idle`/`hydrating`:** O estado `idle` é tratado como transitório e visualmente idêntico ao `hydrating` para garantir que o usuário veja a tela de carregamento desde o primeiro frame do app.
- **Fail-safe no status `error`:** Caso ocorra uma falha crítica na leitura dos tokens (ex: corrupção do SecureStore), o sistema assume o estado `unauthenticated` como medida de segurança, forçando um novo login.
- **TypeScript Hardening:** Configuração do `tsconfig.json` ajustada para suportar JSX e interoperabilidade de módulos sem dependências externas de base, resolvendo conflitos no VS Code.
## 4. Limites da Missão 13
- **UI/UX:** Nenhuma estilização final ou identidade visual foi aplicada.
- **Lógica de Login:** O botão de login na `LoginScreen` permanece como um mock técnico para validar o disparo da action na Store.
- **Navegação:** Limitada a Stacks básicas; Tabs e Drawer não fazem parte deste escopo.

## 5. Próxima Missão (Preview)
**Missão 14 — UI/UX Foundation & Theming:** Definição da paleta de cores nativa, componentes base (Button, Input) e aplicação da identidade visual MesaFlow.

---
*Versão 1.2 — Janeiro de 2026*
