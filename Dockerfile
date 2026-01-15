
# DOMAIN: DEVOPS
# LAST_MODIFIED: 2026-01-13 06:15:00
# Imagem base leve do Python 3.11
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema necessárias para compilação (ex: psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python (Cache Layering)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia todo o código fonte do projeto
COPY . .

# Expõe a porta da API
EXPOSE 8000

# Comando padrão (pode ser sobrescrito pelo docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

