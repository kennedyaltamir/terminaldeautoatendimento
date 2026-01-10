# 🚨 Relatório de Incidente: Tela Preta no Emulador Android (API 36)

**Data:** 10 de Janeiro de 2026  
**Sintoma:** O processo do emulador inicia, os logs de rede (`netsimd`) são gerados, mas a janela do dispositivo permanece estática e preta.

## 1. Análise dos Logs Fornecidos
Os logs indicam que o `netsimd` (Network Simulator Daemon do Android) foi inicializado com sucesso. Isso prova que o binário do emulador está rodando. No entanto, a ausência de logs de "Boot Complete" e a tela preta sugerem uma falha na camada de abstração gráfica ou no estado de hibernação do dispositivo virtual.

## 2. As 5 Principais Causas Prováveis

### 2.1. Incompatibilidade de Aceleração Gráfica (GPU)
O emulador tenta usar a GPU do host (Windows) para renderizar a interface. Se os drivers de vídeo estiverem desatualizados ou se houver conflito com o OpenGL/Vulkan, a renderização falha silenciosamente, resultando em tela preta.

### 2.2. Estado de "Quick Boot" Corrompido
O Android Emulator salva o estado da RAM ao fechar para abrir mais rápido depois. Se esse snapshot for corrompido (comum em atualizações de SDK), o emulador tenta carregar um estado inválido e trava antes de renderizar o primeiro frame.

### 2.3. Conflito de Virtualização (Hyper-V vs WHPX)
No Windows, o emulador depende do Windows Hypervisor Platform (WHPX). Se o Hyper-V estiver parcialmente ativo ou se houver conflito com outros virtualizadores (VirtualBox/VMware), o kernel do Android não consegue inicializar os drivers de vídeo virtuais.

### 2.4. Instabilidade da API 36 (Vanilla Ice Cream)
A API 36 é extremamente recente. Versões "Preview" ou recém-lançadas do Android possuem bugs conhecidos de kernel que impedem o boot em certas CPUs (especialmente AMD ou Intel de gerações específicas sem suporte a certas instruções de virtualização).

### 2.5. Esgotamento de Recursos (RAM/Disco)
O emulador API 36 exige cerca de 2GB a 4GB de RAM dedicada e alta performance de I/O. Se o disco estiver cheio ou a RAM fragmentada, o processo de boot excede o timeout interno e para de responder.

## 3. Plano de Ação
1. Executar o script de diagnóstico `scripts/diagnosis/debug_emulator.py`.
2. Aplicar o "Cold Boot" (Wipe Data).
3. Ajustar a renderização para "Software" se a GPU falhar.
