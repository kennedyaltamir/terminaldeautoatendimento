# 🎨 Task 15: UI Foundation & Design System

## 1. Filosofia
A UI Foundation do MesaFlow Mobile foi construída sob o princípio de **Pure UI**. Os componentes são burros (stateless em relação ao negócio), agnósticos ao contexto de autenticação e focados puramente em renderização baseada em propriedades.

## 2. Tokens Visuais
Centralizamos a identidade visual em tokens TypeScript. Isso permite que o app mude sua aparência globalmente alterando apenas os arquivos em `src/ui/tokens/`.
- **Cores:** Paleta focada no MesaFlow Orange e fundos Slate escuros para ambientes operacionais.
- **Spacing:** Base de 4px para grids e margens.
- **Typography:** Padronização de pesos e tamanhos de fonte nativa.

## 3. Componentes Base
| Componente | Variantes | Descrição |
| :--- | :--- | :--- |
| `Button` | primary, secondary, ghost, danger | Ação principal com suporte a loading state. |
| `Input` | default, error | Entrada de texto com label e validação visual. |
| `Card` | default, outline | Container para agrupamento de informações. |

## 4. Exemplo de Uso (Referência)
```tsx
import { Button } from '../ui/components/Button';
import { spacing } from '../ui/tokens/spacing';

<Button 
  title="Entrar" 
  onPress={handleLogin} 
  style={{ marginTop: spacing.md }} 
/>
```

## 5. Regras de Expansão (O que NÃO pertence aqui)
- Lógica de formulários (use React Hook Form fora daqui).
- Chamadas de API.
- Navegação entre telas.
- Verificações de Permissão/Roles.

---
*Status: Concluído — Janeiro de 2026*
