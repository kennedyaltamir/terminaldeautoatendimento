# 🎨 Detalhamento Técnico: Branding & Identidade Visual (UX-02)

## 1. Problema Atual
A personalização atual limita-se a 3 cores e 2 imagens. Grandes redes exigem uma experiência "White Label" para que o sistema pareça uma extensão do site oficial.

## 2. Solução Proposta (Aba Geral)
Implementar controles avançados de design que refletem instantaneamente no cardápio público.

### 2.1 Novos Campos e Funcionalidades
- **Favicon Upload:** Permitir o upload de ícones `.ico` ou `.png` para a aba do navegador.
- **Font Selection:** Integração com Google Fonts (seleção entre Serif, Sans e Mono).
- **Border Radius Control:** Slider para definir se a interface será "Quadrada" (0px) ou "Arredondada" (16px).
- **Custom CSS:** Campo de texto para usuários avançados injetarem estilos específicos.

## 3. Arquivos a Alterar/Criar
- `app/models.py`: Adicionar campos `favicon_url`, `font_family`, `border_radius`.
- `app/schemas.py`: Atualizar `CompanyUpdate` e `CompanyPublic`.
- `frontend/src/app/[slug]/menu/page.tsx`: Injetar variáveis de CSS dinâmicas no Root.
- `frontend/src/app/admin/[slug]/settings/page.tsx`: Criar os novos inputs de design.

## 4. Aplicação Prática
O dono de uma cafeteria "Vintage" poderá escolher uma fonte cursiva e bordas quadradas, enquanto uma hamburgueria "Tech" usará fontes geométricas e bordas muito arredondadas.
