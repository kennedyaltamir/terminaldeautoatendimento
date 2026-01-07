# 📱 Task 31: Notificações Push Nativa (FCM)

## 1. Contexto
Implementação da comunicação assíncrona entre o servidor e o aplicativo mobile. O objetivo é garantir que o staff receba alertas operacionais (ex: "Pedido Pronto", "Chamado de Mesa") mesmo quando o aplicativo não está em primeiro plano, aumentando a eficiência da operação.

## 2. Decisões Técnicas
- **Expo Notifications:** Utilizado como abstração para o Firebase Cloud Messaging (FCM).
- **Automatic Registration:** O registro do dispositivo é acoplado ao ciclo de vida da autenticação (`AuthStore`). O token é gerado e enviado ao backend imediatamente após o login ou hidratação da sessão.
- **Security & Privacy:** O token FCM é removido do backend durante o processo de logout, garantindo que notificações sensíveis não sejam entregues a dispositivos que não possuem uma sessão ativa.
- **Foreground Handling:** Configurado o `NotificationHandler` para exibir alertas visuais e sonoros mesmo quando o usuário está com o app aberto, reforçando o sistema de "Atenção Ativa" (Missão 22).

## 3. Arquivos Afetados
- `mobile/src/services/notifications.service.ts` (Novo)
- `mobile/src/store/auth.store.ts` (Integração de ciclo de vida)
- `mobile/package.json` (Novas dependências)

## 4. Política de Testes
[TEST_EXEMPT: Integração com serviços externos de Push (Firebase). A validação deve ser feita via Expo Go utilizando a ferramenta de teste do Expo (https://expo.dev/notifications) enviando o token gerado nos logs do app.]

---
*Fase 11 — Janeiro de 2026*
