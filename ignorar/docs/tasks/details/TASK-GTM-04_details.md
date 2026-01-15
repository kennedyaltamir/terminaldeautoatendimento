# ⚖️ Detalhamento Técnico: Compliance Legal & Comercial (TASK-GTM-04)

## 1. Contexto
Para operar como SaaS e processar pagamentos, o MesaFlow precisa estar em conformidade com a LGPD e as regras das bandeiras de cartão (Visa/Mastercard exigem Termos de Uso visíveis).

## 2. Especificação de Implementação

### 2.1 Páginas Estáticas (Next.js)
Criar rotas públicas otimizadas para SEO e leitura:
- `/terms`: Termos de Uso do SaaS.
- `/privacy`: Política de Privacidade e Cookies.

**Conteúdo Técnico:**
- Usar `@tailwindcss/typography` (`prose`) para formatar textos longos automaticamente.
- Inserir data de "Última Atualização" dinâmica ou estática.

### 2.2 Rodapé (Footer)
Atualizar o componente `Footer.tsx` para incluir:
- Links para `/terms` e `/privacy`.
- Razão Social e CNPJ da empresa (Obrigatório por lei para e-commerce/SaaS no Brasil).
- Link para "Status Page" (pode ser um link para o Twitter/X do suporte inicialmente).

### 2.3 Consentimento de Cookies
Implementar um banner simples de consentimento (LGPD):
- **Lógica:** Verificar `localStorage.getItem('cookie_consent')`.
- **UI:** Banner fixo no rodapé com botão "Aceitar".
- **Comportamento:** Só carregar scripts de Analytics (Google/Meta) após o aceite.

## 3. Plano de Validação
1.  Acessar `/terms` e verificar renderização.
2.  Verificar se o CNPJ está visível no rodapé de todas as páginas públicas.
3.  Testar o fluxo de aceite de cookies em aba anônima.
