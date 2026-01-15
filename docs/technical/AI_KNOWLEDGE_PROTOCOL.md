# 🧠 Protocolo de Base de Conhecimento IA

## 1. Onde reside o conhecimento?
A base de conhecimento operacional que eu (IA) utilizo para entender o projeto MesaFlow OS está no arquivo:
**`todososarquivos.txt`** (na raiz do projeto).

## 2. Como ele é gerado?
Através do script `gerartxt.py`. Este script:
1.  Varre as pastas `app`, `frontend`, `mobile`, `docs` e `scripts`.
2.  Ignora lixo (node_modules, venv, caches).
3.  Concatena tudo em um bundle delimitado por tags `[[MESAFLOW_BEGIN:...]]`.

## 3. Comparação e Auditoria
Para você comparar minha base de conhecimento com a realidade:
1.  Abra o arquivo `todososarquivos.txt`.
2.  Verifique a tag `<!-- TIMESTAMP: ... -->` no topo para saber a data da última varredura.
3.  Qualquer arquivo que não conste nesse bundle é "invisível" para mim, a menos que você o forneça no chat.
