# ⏪ Plano de Rollback: TASK-MAINT-01

## 1. Cenário de Falha
Se um arquivo crítico for movido acidentalmente para a pasta ignorar e o sistema apresentar falhas de execução ou build.

## 2. Procedimento de Reversão Manual
Como a ação realizada é apenas MOVER, a reversão consiste em mover os arquivos de volta para a raiz original.
Exemplo de comando para reverter um arquivo específico:
mv ignorar/nome_do_arquivo.py ./

## 3. Reversão Total
Mover todo o conteúdo da pasta ignorar de volta para a raiz do projeto.
Comando sugerido para sistemas baseados em Unix:
mv ignorar/* ./
No sistema Windows, utilize o Explorador de Arquivos para selecionar todos os itens dentro de ignorar e arrastá-los de volta para a pasta raiz mesaflow.
