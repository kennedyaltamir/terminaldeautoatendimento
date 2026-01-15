# 🚨 Relatório de Incidente: Falha de Política de Runtime (Bare Workflow)

**Data:** 10 de Janeiro de 2026  
**Sintoma:** O Expo Go abre no emulador, mas exibe a tela azul "Something went wrong". O terminal reporta um erro de `CommandError` relacionado à `runtimeVersion`.

## 1. Diagnóstico da Causa Raiz
O erro ocorre porque o projeto está sendo detectado como **Bare Workflow** (provavelmente pela presença de pastas nativas ou configurações de build customizadas). 

No Bare Workflow, o Expo **não permite** o uso de políticas automáticas para a versão de runtime, como `{"policy": "appVersion"}`. Ele exige que a versão seja uma **string estática** (ex: "1.0.0"). Isso é necessário para que as atualizações OTA (Over-the-Air) saibam exatamente com qual build nativo elas são compatíveis.

## 2. As 5 Possibilidades de Falha Analisadas

### 2.1. Configuração de Runtime Dinâmica (Confirmado)
O arquivo `app.json` está tentando usar uma política de versão que só funciona no "Managed Workflow". Como o sistema detectou o modo "Bare", o bundler recusa a inicialização.

### 2.2. Cache do Metro Bundler
Mesmo corrigindo o arquivo, o Metro pode manter uma versão "suja" da configuração em memória, exigindo um reset de cache.

### 2.3. Descompasso de Versão do Expo SDK
O projeto usa SDK 52, mas algumas dependências podem estar pedindo recursos de versões superiores ou inferiores que forçam o comportamento de Bare Workflow.

### 2.4. Conflito de Identificadores (Bundle ID)
Se o `slug` no `app.json` não bater com o nome do projeto no diretório, o Expo Go se confunde ao tentar baixar o manifesto.

### 2.5. Erro de Rede (IP do Host)
O emulador às vezes falha ao conectar no IP `192.168.0.150` se houver múltiplas interfaces de rede (VPN, Docker, etc) ativas no Windows.

## 3. Plano de Resolução
1. Corrigir o `mobile/app.json` para usar uma versão de runtime estática.
2. Limpar o cache do Expo e do Metro.
3. Forçar o túnel local se o IP falhar.
