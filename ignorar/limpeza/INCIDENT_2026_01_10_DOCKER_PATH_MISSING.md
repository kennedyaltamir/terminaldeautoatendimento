# 🚨 Relatório de Incidente: Comando 'docker' não reconhecido

**Data:** 10 de Janeiro de 2026  
**Sintoma:** O terminal PowerShell retorna `CommandNotFoundException` para o binário `docker`, apesar do Docker Desktop estar em execução.

## 1. Diagnóstico da Causa Raiz
O Windows carrega as variáveis de ambiente (incluindo o `PATH` onde o Docker reside) apenas no momento da abertura do processo do terminal. Como o terminal foi aberto antes ou durante a instalação do Docker Desktop, ele não possui a referência para `C:\Program Files\Docker\Docker\resources\bin`.

## 2. Procedimento de Resolução (Obrigatório)

### Passo 1: Reinicialização do Processo de Terminal
1. Feche **todas** as janelas do PowerShell, CMD ou terminais integrados do VS Code.
2. Abra um **novo** terminal PowerShell.
3. Navegue de volta para a pasta do projeto: `cd C:\mesaflow`.
4. Reative o ambiente virtual: `.\.venv\Scripts\activate`.

### Passo 2: Verificação de Integração WSL 2
Se após reiniciar o terminal o erro persistir:
1. Abra o **Docker Desktop**.
2. Vá em **Settings** (ícone de engrenagem) > **Resources** > **WSL Integration**.
3. Garanta que a opção "Enable integration with my default WSL distro" está marcada.
4. Clique em "Apply & Restart".

### Passo 3: Execução do Setup
No novo terminal, execute:
```powershell
python scripts/setup/setup_redis.py
```

## 3. Verificação Manual de PATH (Último Recurso)
Se o comando `docker --version` ainda falhar em um novo terminal, execute este comando para adicionar temporariamente ao PATH da sessão atual:
```powershell
$env:Path += ";C:\Program Files\Docker\Docker\resources\bin"
```
