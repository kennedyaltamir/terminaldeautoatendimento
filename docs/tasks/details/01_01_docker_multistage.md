# 🏗️ Detalhamento Técnico: Docker Multi-stage Build

## 1. Problema Atual
A imagem Docker atual carrega ferramentas de compilação, caches de pacotes e dependências de desenvolvimento para o ambiente de produção. Isso resulta em:
- Imagens pesadas (>1GB).
- Maior superfície de ataque (presença de compiladores e shells desnecessários).
- Tempo de deploy elevado.

## 2. Solução Proposta
Implementar o padrão **Multi-stage Build** no `Dockerfile`.

### Estágio 1: Builder
- Base: `python:3.11-slim`.
- Ação: Instalar `gcc`, `libpq-dev` e outras dependências de compilação.
- Resultado: Gerar os *wheels* (binários) do Python em uma pasta temporária.

### Estágio 2: Runtime
- Base: `python:3.11-slim` (limpa).
- Ação: Copiar apenas os pacotes instalados do estágio anterior.
- Segurança: Criar um usuário `mesaflow` sem privilégios de root para rodar a aplicação.

## 3. Impactos e Performance
- **Tamanho:** Redução estimada de 70% no tamanho da imagem.
- **Velocidade:** Pull da imagem no servidor de produção será 3x mais rápido.
- **Segurança:** Remoção de binários de compilação impede que atacantes compilem exploits caso invadam o container.

## 4. Critérios de Aceite
- [ ] Imagem final abaixo de 250MB.
- [ ] Aplicação rodando com usuário não-root.
- [ ] Build bem-sucedido no CI/CD.
