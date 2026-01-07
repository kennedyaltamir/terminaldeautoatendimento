# 🧪 Roteiro de Teste Manual (Smoke Test) - MesaFlow Mobile

## 1. Ciclo de Autenticação
- [ ] **Login:** Inserir credenciais válidas. *Esperado: Transição para Home/KDS.*
- [ ] **Persistência:** Fechar o app e abrir novamente. *Esperado: Manter logado (Hydration).*
- [ ] **Logout:** Clicar em sair. *Esperado: Limpeza do SecureStore e volta para tela de Login.*

## 2. Modo KDS (Cozinha)
- [ ] **Recebimento:** Criar pedido via Web Admin. *Esperado: Pedido aparecer no Mobile em < 2s.*
- [ ] **SLA:** Aguardar 5 minutos. *Esperado: Card mudar de cor (Verde -> Amarelo).*
- [ ] **Ação:** Clicar em "Avançar". *Esperado: Status mudar no banco e refletir no Web Admin.*
- [ ] **Alerta:** Deixar pedido atrasar. *Esperado: Dispositivo vibrar (se suportado pelo emulador).*

## 3. Modo POS (Garçom)
- [ ] **Mesas:** Abrir o mapa de mesas. *Esperado: Sincronia com o salão real.*
- [ ] **Lançamento:** Adicionar 3 itens ao carrinho e enviar. *Esperado: Pedido aparecer no KDS.*
- [ ] **Pagamento:** Gerar QR Code Pix. *Esperado: QR Code renderizado na tela.*

## 4. Resiliência Offline
- [ ] **Corte de Rede:** Desativar Wi-Fi do emulador. *Esperado: Banner "Conexão Perdida" aparecer.*
- [ ] **Fila Offline:** Lançar pedido sem rede. *Esperado: Tela de "Pedido em Fila".*
- [ ] **Sincronia:** Reativar Wi-Fi. *Esperado: Pedido ser enviado automaticamente (Background Sync).*
