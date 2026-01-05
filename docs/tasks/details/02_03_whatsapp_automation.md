# 📱 Detalhamento Técnico: Automação & Templates WhatsApp (UX-03)

## 1. Problema Atual
As mensagens enviadas são fixas no código. O usuário não pode personalizar o tom de voz da marca ou incluir links promocionais.

## 2. Solução Proposta (Aba Marketing)
Transformar a configuração de WhatsApp em um centro de engajamento.

### 2.1 Funcionalidades
- **Template Editor:** Textarea para editar as mensagens de "Pedido Recebido", "Pronto" e "Saiu para Entrega".
- **Variáveis Dinâmicas:** Suporte a tags como `{{cliente}}`, `{{pedido_id}}`, `{{total}}`.
- **Health Check:** Botão "Testar Conexão" que envia uma mensagem de teste para o número do dono.
- **Status da Instância:** Indicador visual (Verde/Vermelho) se a API Evolution está conectada.

## 3. Arquivos a Alterar/Criar
- `app/models.py`: Adicionar campos `template_ready`, `template_dispatch`.
- `app/services/whatsapp_service.py`: Lógica de parser de variáveis `{{}}`.
- `frontend/src/components/admin/WhatsAppTester.tsx`: Novo componente de diagnóstico.

## 4. Testes
- Validar se o parser substitui corretamente as variáveis.
- Validar comportamento quando a API de WhatsApp retorna erro 401 (Token expirado).
