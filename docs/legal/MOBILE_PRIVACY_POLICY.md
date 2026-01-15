
# 📱 Política de Privacidade — MesaFlow Mobile
**Versão:** 1.0 (Enterprise Compliance)
**Última Atualização:** 11 de Janeiro de 2026

Esta política descreve como o aplicativo MesaFlow trata dados em dispositivos móveis.

## 1. Coleta de Dados Mínima (Data Minimization)
O MesaFlow Mobile coleta apenas o estritamente necessário para a operação do restaurante:
- **Identificação:** Nome e Cargo (via JWT).
- **Operacional:** Pedidos lançados e status de produção.
- **Técnico:** Device ID para notificações Push e logs de erro (Sentry).

## 2. Uso de Permissões Nativas
- **Câmera:** Utilizada exclusivamente para leitura de QR Codes de mesa. Nenhuma imagem é armazenada ou enviada para nossos servidores.
- **Vibração:** Utilizada para alertas operacionais (Pedido Pronto / Chamado de Mesa).
- **Internet:** Necessária para sincronização em tempo real com o Kernel MesaFlow.

## 3. Isolamento e Segurança
- **Multi-tenancy:** Seus dados são isolados via Row-Level Security (RLS) no nível do banco de dados.
- **Criptografia:** Todos os dados em trânsito utilizam TLS 1.2+ (HTTPS/WSS). Tokens de sessão são armazenados no SecureStore (Hardware-backed encryption).

## 4. Seus Direitos (LGPD)
O usuário pode solicitar a exclusão de sua conta e dados vinculados através do administrador do seu estabelecimento ou pelo e-mail `dpo@mesaflow.com.br`.

---
*MesaFlow Tecnologia Ltda.*

