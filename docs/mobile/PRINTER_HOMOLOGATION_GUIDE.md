# 🖨️ Guia de Homologação de Impressão (Missão 37)

Este guia orienta o teste de hardware real utilizando o binário nativo do MesaFlow.

## 1. Preparação
1.  Instale o APK no seu dispositivo Android.
2.  Ligue a impressora térmica Bluetooth e certifique-se de que ela está em modo de pareamento.
3.  Abra o App MesaFlow e realize o login.

## 2. Execução do Teste
1.  Acesse o menu lateral (ou atalho de suporte) e entre em **"Debug de Hardware"**.
2.  Clique no ícone de **Recarregar (Refresh)** para buscar dispositivos.
3.  Selecione a sua impressora na lista.
4.  Clique em **"Disparar Teste de Impressão"**.

## 3. O que validar no papel?
- [ ] **Alinhamento:** O nome do restaurante deve estar centralizado.
- [ ] **Acentuação:** Palavras como "Café" ou "Atenção" não devem ter símbolos estranhos.
- [ ] **Densidade:** O texto em modo `LARGE` deve estar nítido.
- [ ] **Corte:** A impressora deve avançar o papel e realizar o corte (se suportado).

## 4. Resolução de Problemas (Logs)
Se a impressão falhar, conecte o celular ao PC e monitore via VS Code:
`adb logcat *:S ReactNative:V ReactNativeJS:V`
Procure por logs da tag `[BluetoothService]` ou `[PrinterService]`.
