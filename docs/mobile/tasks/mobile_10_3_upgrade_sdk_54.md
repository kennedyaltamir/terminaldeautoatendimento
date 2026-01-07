# 📱 Task 10.3: Upgrade para Expo SDK 54

## 1. Contexto
Detectada incompatibilidade entre o ambiente de desenvolvimento (SDK 51) e a versão do cliente Expo Go disponível nas lojas (SDK 54). O upgrade é necessário para permitir o teste em dispositivos físicos.

## 2. Decisões Técnicas
- **Upgrade Direto:** Pulamos as versões intermediárias para alinhar com o Expo Go v54.
- **Version Alignment:** Utilização do comando `npx expo install --fix` para garantir que as dependências nativas (peer dependencies) estejam em conformidade com o novo SDK.

## 3. Impactos
- **Melhoria de Performance:** O SDK 54 traz otimizações no motor de renderização e no tempo de inicialização.
- **Compatibilidade:** Suporte total às versões mais recentes do Android e iOS.

## 4. Arquivos Afetados
- `mobile/package.json`

---
*Manutenção de Infraestrutura — Janeiro de 2026*
# 📱 Task 10.3: Upgrade para Expo SDK 54 (Re-execução)

## 1. Contexto
Incompatibilidade persistente entre o projeto e o Expo Go v54. Forçado upgrade manual das dependências no `package.json`.

## 2. Decisões Técnicas
- **Hard Reset:** Recomendação de limpeza de `node_modules` e `.expo` para eliminar metadados do SDK 51.
- **Explicit Versioning:** Definição de versões fixas para `react-native` e `expo` para evitar que o `npm` tente manter versões antigas.

## 3. Status
- [x] Atualização de `package.json` para SDK 54.
- [ ] Limpeza de cache local e re-instalação.

---
*Manutenção de Infraestrutura — Janeiro de 2026*
# 📱 Task 10.3: Upgrade para Expo SDK 54 (Finalização)

## 1. Contexto
Resolução de conflitos de dependências e pacotes ausentes após o upgrade para o SDK 54.

## 2. Decisões Técnicas
- **Navigation Sync:** Reintrodução dos pacotes `@react-navigation` que haviam sido removidos do manifesto.
- **Babel Alignment:** Atualização do `babel-preset-expo` para a versão `~54.0.9` para compatibilidade com o novo motor de build.
- **React 19 Support:** Manutenção do uso de `--legacy-peer-deps` devido às mudanças profundas no ecossistema React 19.

## 3. Status
- [x] Atualização de `package.json` com navegação e babel corrigidos.
- [x] Sincronização de versões nativas.

---
*Manutenção de Infraestrutura — Janeiro de 2026*
# 📱 Task 10.3: Upgrade para Expo SDK 54 (Finalização)

## 1. Contexto
Resolução de conflitos de dependências e pacotes ausentes após o upgrade para o SDK 54.

## 2. Decisões Técnicas
- **Navigation Sync:** Reintrodução dos pacotes `@react-navigation` compatíveis com React 19.
- **Babel Alignment:** Atualização do `babel-preset-expo` para a versão `~54.0.9`.
- **JWT Utility Fix:** Criação do `mobile/src/lib/jwt.ts` utilizando a biblioteca `base-64` para suprir a ausência de `window.atob` no ambiente nativo.

## 3. Status
- [x] Atualização de `package.json` com navegação e babel corrigidos.
- [x] Implementação do decodificador JWT nativo.
- [x] Sincronização de versões nativas.

---
*Manutenção de Infraestrutura — Janeiro de 2026*
# 📱 Task 10.3: Upgrade para Expo SDK 54 (Finalização)

## 1. Contexto
Resolução de conflitos de dependências e pacotes ausentes após o upgrade para o SDK 54.

## 2. Decisões Técnicas
- **Navigation Sync:** Reintrodução dos pacotes `@react-navigation` compatíveis com React 19.
- **Babel Alignment:** Atualização do `babel-preset-expo` para a versão `~54.0.9`.
- **JWT Utility Fix:** Criação do `mobile/src/lib/jwt.ts` utilizando a biblioteca `base-64`.
- **SVG Dependency Fix:** Inclusão do pacote `react-native-svg` exigido pela biblioteca `lucide-react-native` para renderização de ícones.

## 3. Status
- [x] Atualização de `package.json` com navegação, babel e SVG corrigidos.
- [x] Implementação do decodificador JWT nativo.
- [x] Sincronização de versões nativas.

---
*Manutenção de Infraestrutura — Janeiro de 2026*
