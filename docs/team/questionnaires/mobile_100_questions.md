# 📱 Questionário de Auditoria: Mobile Engineer (100 Perguntas)
**Foco:** React Native, Expo SDK 54, Offline-first, Hardware e Resiliência Operacional.

## Seção 1: React Native & Expo Core (20 Perguntas)
1. Qual a principal vantagem do Expo Managed Workflow para o MesaFlow?
2. O que é a "New Architecture" (Fabric/TurboModules) e como ela impacta o app?
3. Como o `app.json` configura as permissões nativas de Bluetooth e Câmera?
4. Explique o funcionamento do Metro Bundler durante o desenvolvimento.
5. Como o Expo SDK 54 lida com a compatibilidade entre Android e iOS?
6. O que é o "EAS Build" e por que o utilizamos em vez de builds locais puros?
7. Como o `expo-updates` permite enviar correções críticas sem passar pela App Store?
8. Qual a função do `expo-constants` na gestão de variáveis de ambiente?
9. Como o React Native gerencia a renderização de componentes nativos?
10. O que é o "Bridge" e como a New Architecture pretende eliminá-lo?
11. Como otimizar o tempo de inicialização (T01 - Cold Start) do aplicativo?
12. Como o Expo lida com ícones e Splash Screens de diferentes densidades?
13. Como configurar o "Deep Linking" para abrir o app via QR Code de mesa?
14. O que são "Config Plugins" no Expo e quando precisamos deles?
15. Como o React Native lida com o gerenciamento de memória em listas longas?
16. Como debugar o código nativo usando o Flipper ou React DevTools?
17. Qual a importância do `runtimeVersion` na estratégia de atualizações OTA?
18. Como o Expo gerencia as chaves de assinatura (.keystore / .p12) no EAS?
19. Como implementar o "Haptic Feedback" para confirmação de pedidos?
20. Como o app lida com a mudança de orientação da tela (Portrait vs Landscape)?

## Seção 2: Estado Global & Offline-First (20 Perguntas)
21. Por que escolhemos Zustand para o estado global mobile?
22. Como o `persist` middleware do Zustand salva os dados no `AsyncStorage`?
23. O que é o "Hydration" no Zustand e como ele previne telas em branco no boot?
24. Como o app lida com a persistência de tokens JWT no `Expo SecureStore`?
25. Explique a estratégia de "State Reconciliation" ao reconectar à internet.
26. Como o `TanStack Query` (React Query) gerencia o cache de pedidos no mobile?
27. Como implementar uma fila de sincronização (Sync Queue) para pedidos offline?
28. O que acontece se o app for fechado enquanto um pedido está sendo sincronizado?
29. Como o app detecta mudanças no estado da rede (NetInfo)?
30. Como evitar que o estado local divirja da verdade do servidor (Server-Wins)?
31. Como o app lida com o armazenamento de imagens em cache para uso offline?
32. Qual a diferença entre `AsyncStorage` e `SecureStore` em termos de segurança?
33. Como implementar o "Optimistic UI" no avanço de status do KDS?
34. Como o app lida com conflitos de dados (ex: dois garçons editando o mesmo item)?
35. Como o sistema garante que o garçom não perca o carrinho se a bateria acabar?
36. Como o app lida com a expiração do token enquanto o dispositivo está offline?
37. Como o `GlobalClockService` sincroniza o tempo entre o dispositivo e o servidor?
38. Como o app lida com grandes volumes de dados no `AsyncStorage` (> 6MB)?
39. Como implementar um "Background Task" para sincronizar dados em segundo plano?
40. Como o app garante a integridade referencial dos IDs de produtos em modo offline?

## Seção 3: Hardware & Integrações Nativas (20 Perguntas)
41. Como o app se comunica com impressoras térmicas via Bluetooth (BLE)?
42. O que é o protocolo ESC/POS e como geramos o buffer de impressão?
43. Como o app lida com a descoberta e pareamento de novos dispositivos Bluetooth?
44. Como implementar a impressão de etiquetas ZPL para delivery?
45. Como o app interage com a gaveta de dinheiro (Cash Drawer) via impressora?
46. Como funciona a integração com maquininhas de cartão (SmartPOS SDK)?
47. Como o app captura a localização GPS do entregador sem drenar a bateria?
48. Como o app utiliza a câmera para escanear QR Codes de mesas e produtos?
49. Como o app lida com a permissão de "Always On" para a tela do KDS?
50. Como integrar balanças de precisão via Bluetooth no módulo de pesagem?
51. Como o app lida com a desconexão da impressora no meio de uma impressão?
52. Como formatar o cupom para diferentes larguras de papel (58mm vs 80mm)?
53. Como o app lida com a fila de impressão para evitar travamentos da UI?
54. Como implementar o som de alerta ("Ding") no KDS usando `expo-av`?
55. Como o app interage com o sistema de biometria (FaceID/Fingerprint) para login?
56. Como o app lida com a detecção de "NFC" para pagamentos por aproximação?
57. Como o app garante que o som de alerta toque mesmo se o celular estiver no silencioso?
58. Como o app lida com a atualização de firmware de periféricos homologados?
59. Como implementar o modo "Kiosk" (App Lock) para totens de autoatendimento?
60. Como o app lida com a impressão de caracteres especiais e acentos em ESC/POS?

## Seção 4: Real-time & SLA Engine (20 Perguntas)
61. Como o app mantém a conexão WebSocket estável em redes móveis (3G/4G)?
62. Explique a estratégia de "Exponential Backoff" para reconexão do socket.
63. Como o app processa eventos de `new_order` vindos do Redis Pub/Sub?
64. O que é o `GlobalClockService` e por que ele é vital para o KDS?
65. Como o app calcula o `priorityScore` de um pedido em tempo real?
66. Como o app lida com a mudança de cores dos cards baseada no tempo de SLA?
67. Como o app garante que o alerta de "Pedido Atrasado" seja disparado no momento exato?
68. Como o app lida com o "Cooldown" de vibração para não irritar o cozinheiro?
69. Como o app sincroniza o status de "Preparando" entre o tablet e o celular do garçom?
70. Como o app lida com a recepção de mensagens WebSocket enquanto está em background?
71. Como o app filtra eventos de WebSocket para garantir que receba apenas dados do seu Tenant?
72. Como o app lida com a "Tempestade de Eventos" (muitos pedidos ao mesmo tempo)?
73. Como o app garante que a lista de pedidos esteja sempre ordenada por urgência?
74. Como o app lida com a atualização de um pedido que não está mais na memória local?
75. Como o app notifica o garçom que uma mesa chamou por ajuda (waiter_call)?
76. Como o app lida com a latência de rede na confirmação de uma ação do operador?
77. Como o app garante que o WebSocket não seja encerrado pelo sistema operacional?
78. Como o app lida com a mudança de status de um pedido feita via Web Admin?
79. Como o app exibe o indicador de "Conectado/Desconectado" para o operador?
80. Como o app lida com a recepção de payloads grandes via WebSocket?

## Seção 5: Qualidade, SRE & Release (20 Perguntas)
81. O que é o `PRODUCTION_LOCK_MOBILE.json` e qual sua importância?
82. Como o Sentry captura "Native Crashes" (C++) no Android/iOS?
83. Como o `LoggerService` ajuda no diagnóstico de problemas em campo?
84. O que é o "UI Sweep" e como ele valida a renderização de todas as telas?
85. Como o app lida com o "Error Boundary" global para evitar o fechamento abrupto?
86. Como o app reporta a saúde da bateria e do sinal Wi-Fi para o Admin?
87. Como funciona o pipeline de CI/CD para gerar o APK de teste automaticamente?
88. Como o app lida com a ofuscação de código (Proguard/R8) em produção?
89. Como o app garante que nenhuma credencial sensível vaze nos logs do Logcat?
90. Como o app lida com a expiração forçada de versões antigas (Force Update)?
91. Como o app lida com o teste de carga simulando centenas de pedidos no KDS?
92. Como o app garante a conformidade com as diretrizes de design da Apple (HIG)?
93. Como o app lida com a privacidade de dados (Data Safety) nas lojas?
94. Como o app lida com o monitoramento de performance (TTI, Frame Drops)?
95. Como o app garante que o "Silent Mode" do operador seja respeitado?
96. Como o app lida com a auditoria de ações do staff (quem deu baixa no pedido)?
97. Como o app lida com a restauração de estado após um crash inesperado?
98. Como o app garante que o bundle de JS seja o menor possível (Tree Shaking)?
99. Como o app lida com a segurança de rede (SSL Pinning) em redes públicas?
100. Por que o MesaFlow Mobile é considerado um "Sistema de Missão Crítica"?

