# 🚀 Guia de Inicialização do App no Emulador

Se o emulador abriu mas você não vê o ícone do "MesaFlow", é porque em modo de desenvolvimento usamos o **Expo Go** como hospedeiro.

## Passo 1: Iniciar o Servidor de Desenvolvimento (Metro)
Abra um terminal na pasta `mobile/` e execute:
```bash
npx expo start
```
Mantenha este terminal aberto. Ele é o "coração" que envia o código para o celular.

## Passo 2: Abrir no Android
Existem duas formas de fazer o app aparecer na tela:

### Opção A: Atalho do Teclado (Recomendado)
No terminal onde o Expo está rodando, simplesmente pressione a tecla **`a`**.
O Expo irá:
1. Detectar o emulador aberto.
2. Instalar o app "Expo Go" (se não existir).
3. Abrir o MesaFlow automaticamente.

### Opção B: Script de Força Bruta (Se a Opção A falhar)
Se você pressiona `a` e nada acontece, use o script que criamos:
```bash
python scripts/automation/launch_mobile_app.py
```

## O que esperar?
1. A tela do Android Studio deve abrir o aplicativo **Expo Go**.
2. Você verá uma barra de progresso "Building JavaScript bundle".
3. A tela de **Login do MesaFlow** aparecerá.

---
*Nota: Se o Expo Go pedir login, você pode ignorar ou criar uma conta gratuita na Expo, mas geralmente ele abre o "Local Project" automaticamente.*
