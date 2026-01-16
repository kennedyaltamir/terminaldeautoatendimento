# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-15 15:25:00
# 🩺 Relatório de Incidente: UnicodeDecodeError (Byte 0xe7)

## 1. Descrição
O sistema falhou ao iniciar a conexão com o banco de dados e ao processar o loop do iFood devido a um erro de decodificação de caracteres no Windows. O byte `0xe7` (caractere `ç`) estava presente em variáveis de ambiente ou no arquivo `.env`, causando o crash do driver `psycopg2`.

## 2. Causa Raiz
O arquivo `.env` foi salvo ou editado em um editor que utiliza o encoding padrão do Windows (CP1252), enquanto o Kernel MesaFlow e as bibliotecas Python esperam UTF-8 estrito.

## 3. Ações Corretivas
- **Database Layer:** Adicionado `client_encoding: utf8` nos argumentos de conexão do SQLAlchemy.
- **Environment:** Criado script `fix_env_encoding.py` para normalizar o arquivo `.env` no disco.
- **Dotenv:** Forçada a leitura do `load_dotenv` com encoding UTF-8.

## 4. Veredito
O sistema agora é resiliente a caracteres especiais em credenciais e caminhos de diretório no Windows.

