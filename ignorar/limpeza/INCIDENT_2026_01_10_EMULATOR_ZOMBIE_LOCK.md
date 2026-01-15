# 🚨 Relatório de Incidente: Bloqueio de AVD por Processos Zumbis

**Data:** 10 de Janeiro de 2026  
**Sintoma:** O emulador falha ao iniciar com erro `FATAL | Running multiple emulators with the same AVD` e a tela permanece preta.

## 1. Diagnóstico da Causa Raiz
O erro `FATAL` nos seus logs indica que o Android Studio acredita que o emulador **já está rodando**. 
Quando você fecha o emulador ou ele trava (tela preta), o processo `qemu-system-x86_64.exe` pode continuar rodando em segundo plano (processo zumbi). 

Enquanto esse processo existir, ele mantém um "lock" (trava) nos arquivos do disco. Tentar abrir o emulador novamente resulta no erro de "múltiplas instâncias", impedindo qualquer tentativa de correção como o `-wipe-data`.

## 2. As 5 Possibilidades de Falha (Ordenadas por Probabilidade)

### 2.1. Processos Zumbis e Arquivos .lock (Confirmado pelos Logs)
O emulador cria arquivos `.lock` na pasta do AVD para impedir corrupção. Se o processo cai mas o arquivo fica lá, o emulador não abre mais.

### 2.2. Incompatibilidade de Driver NVIDIA (RTX 3060)
Seu log mostra a GPU RTX 3060. Versões recentes do driver NVIDIA às vezes conflitam com a aceleração Vulkan do emulador API 36, exigindo o fallback para OpenGL.

### 2.3. Instabilidade da API 36
A API 36 é a versão mais recente (Android 15/16 Preview). Ela é inerentemente instável e pode falhar no "Cold Boot" em certas configurações de hardware.

### 2.4. Conflito de Snapshot (Quick Boot)
O emulador tenta carregar o estado anterior da memória que está corrompido, resultando na tela preta infinita.

### 2.5. Permissões de Pasta Temporária
O log mostra o caminho `AppData\Local\Temp\netsimd`. Se o Windows bloquear a escrita nessa pasta temporária, o subsistema de rede do Android trava o boot.

## 3. Plano de Resolução
1. Matar todos os processos de emulação.
2. Deletar manualmente os arquivos de trava (`.lock`).
3. Forçar um boot limpo com renderização estável.
