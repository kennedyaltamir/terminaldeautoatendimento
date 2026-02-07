# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 18:21:54
"""
Configurações de Metadados para a Documentação da API (Swagger/OpenAPI).
Este arquivo define como a documentação interativa (/docs) é apresentada.
"""

tags_metadata = [
    {
        "name": "Public",
        "description": "Endpoints acessíveis pelo **Cliente Final**. Permite consultar cardápio, realizar check-in e fazer pedidos sem login administrativo.",
    },
    {
        "name": "Authentication",
        "description": "Gestão de Sessão. Inclui Login via E-mail/Senha, **Google Login** e renovação de tokens.",
    },
    {
        "name": "Admin Orders",
        "description": "Operação de Cozinha (KDS). Monitoramento e controle de status de produção em tempo real.",
    },
    {
        "name": "Admin Menu",
        "description": "Engenharia de Cardápio. Gestão de Categorias, Produtos, Adicionais e Ficha Técnica.",
    },
    {
        "name": "Admin Tables",
        "description": "Gestão de Salão. Controle de Mesas, sessões de clientes e chamados de garçom.",
    },
    {
        "name": "Admin Metrics",
        "description": "Business Intelligence. Dashboards financeiros, métricas operacionais e exportação de dados.",
    },
    {
        "name": "Admin Finance",
        "description": "Configurações SaaS. Gestão de Planos (Stripe), Split de Pagamento e faturamento de comissões.",
    },
    {
        "name": "Integrations",
        "description": "Comunicação Externa. Webhooks para Stripe, Mercado Pago e automação de WhatsApp.",
    },
]

api_description = """
# 🚀 MesaFlow API v2.3.0
O Sistema Operacional para Food Service e Ambientes de Alto Tráfego.

## 🔑 Autenticação
A maioria das rotas administrativas requer um token **Bearer JWT**.
Para obter um token, utilize o endpoint `/api/auth/token` ou `/api/auth/google`.

## 📡 WebSockets
Para receber atualizações em tempo real (Novos Pedidos/KDS), conecte-se em:
`ws://{host}/api/ws/{company_slug}`

## 🛡️ Segurança Multi-tenant
Todos os recursos são isolados via `company_id`. 
É impossível acessar dados de uma empresa usando o token de outra.
"""
