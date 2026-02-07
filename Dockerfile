# Base Python
FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia todos os arquivos da API para dentro do container
COPY . .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta da API
EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
