# ⚙️ Módulo: Configurações Gerais
**Rotas:** `/admin/[slug]/settings`

## 1. Identidade Visual
- **Intenção:** Customização White-label da loja.
- **Elementos:**
    - **ColorPickers:** Cor primária, fundo e texto.
    - **Logo/Banner Upload:** Drag & drop para imagens da marca.
- **Comportamento:** Preview em tempo real do cardápio PWA em uma janela lateral.

## 2. Operacional
- **Intenção:** Regras de funcionamento do estabelecimento.
- **Elementos:**
    - **TimePicker:** Horário de abertura e fechamento.
    - **Taxa de Entrega:** Valor fixo ou dinâmico.
    - **Configuração de Wi-Fi:** SSID e Senha para exibir no QR Code.

## 3. APIs Consumidas
- `GET /api/admin/company/me`: Dados atuais.
- `PATCH /api/admin/company/me`: Persistência das alterações.
