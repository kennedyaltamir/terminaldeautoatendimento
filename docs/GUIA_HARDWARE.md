# 🖨️ Guia de Hardware e Impressão

Requisitos técnicos para rodar o MesaFlow com estabilidade.

---

## 1. Impressão Térmica (Android/Mobile)
Para garçons imprimirem a conta direto do celular ou para tablets na cozinha.

**Recomendação:** Usar o app **RawBT** (Disponível na Play Store).

### Passo a Passo de Configuração:
1.  Instale o **RawBT Driver for Thermal Printer**.
2.  Pareie sua impressora Bluetooth com o celular Android.
3.  Abra o RawBT > Configurações > Conexão > Escolha "Bluetooth" e selecione sua impressora.
4.  Faça um teste de impressão dentro do app RawBT.
5.  No MesaFlow, ative o "Servidor de Impressão" nas configurações do RawBT (Porta 9100 ou API Local).
6.  No App do Garçom, ao clicar em "Imprimir", o sistema enviará o comando direto para o RawBT.

---

## 2. Impressão via PC (Windows/Browser)
Para o caixa que usa computador.

1.  Instale o driver da impressora (Epson, Bematech, Elgin) no Windows.
2.  No Chrome, pressione `Ctrl+P` na tela de pedido.
3.  **Configurações Obrigatórias:**
    *   **Destino:** Selecione a impressora térmica.
    *   **Tamanho do Papel:** 80mm ou 58mm (conforme sua bobina).
    *   **Margens:** "Nenhuma" ou "Mínima".
    *   **Cabeçalho e Rodapé:** Desmarque esta opção (para não sair a URL no papel).

---

## 3. Requisitos de Tablets (KDS)
Não compre tablets muito antigos, pois o sistema usa tecnologias modernas (WebSockets/Animações).

*   **Recomendado:** Samsung Galaxy Tab A7/A8 ou iPad (9ª geração ou superior).
*   **Mínimo:** Android 10+, 3GB RAM, Tela HD.
*   **Navegador:** Use sempre o **Google Chrome** ou **Kiosk Browser** (para travar a tela no sistema).

---

## 4. Rede e Wi-Fi
O sistema depende de internet para processar pagamentos e sincronizar a cozinha.

*   **Rede Dedicada:** Tenha um Wi-Fi exclusivo para a operação (Tablets/Impressoras) separado do Wi-Fi de Clientes. Isso evita lentidão quando a casa enche.
*   **Backup:** Tenha um celular com 4G disponível para rotear internet caso a fibra caia. O sistema consome poucos dados.