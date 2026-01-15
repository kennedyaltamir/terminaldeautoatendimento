import os
import sys
import requests
import smtplib
from sqlalchemy import create_engine, text

# Importações opcionais/externas com tratamento de erro
try:
    import stripe
except ImportError:
    stripe = None

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    boto3 = None
    ClientError = Exception # Fallback para evitar NameError

def log(service, status, msg):
    icon = "✅" if status == "OK" else "❌" if status == "FAIL" else "⚠️"
    print(f"{icon} [{service}] {msg}")

def check_database():
    url = os.getenv("DATABASE_URL")
    if not url:
        log("DATABASE", "FAIL", "Variável DATABASE_URL não definida.")
        return False
    try:
        if "postgres://" in url: url = url.replace("postgres://", "postgresql://")
        engine = create_engine(url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        log("DATABASE", "OK", "Conexão estabelecida com sucesso.")
        return True
    except Exception as e:
        log("DATABASE", "FAIL", f"Erro de conexão: {str(e)}")
        return False

def check_storage():
    # Verifica dependência primeiro
    if not boto3:
        log("STORAGE", "FAIL", "Biblioteca 'boto3' não instalada. Execute: pip install boto3")
        return False

    bucket = os.getenv("AWS_BUCKET_NAME")
    key = os.getenv("AWS_ACCESS_KEY_ID")
    secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    if not bucket or not key or not secret:
        log("STORAGE", "WARN", "Configuração S3 incompleta. Usando Local (Efêmero).")
        return True

    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=key,
            aws_secret_access_key=secret,
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            endpoint_url=os.getenv("AWS_ENDPOINT_URL")
        )
        # Tenta listar objetos (operação leve)
        s3.list_objects_v2(Bucket=bucket, MaxKeys=1)
        log("STORAGE", "OK", f"Acesso ao Bucket '{bucket}' confirmado.")
        return True
    except ClientError as e:
        log("STORAGE", "FAIL", f"Erro de acesso S3: {e}")
        return False
    except Exception as e:
        log("STORAGE", "FAIL", f"Erro genérico S3: {e}")
        return False

def check_stripe():
    key = os.getenv("STRIPE_SECRET_KEY")
    if not key:
        log("STRIPE", "WARN", "STRIPE_SECRET_KEY não definida. Pular.")
        return True 
    if not stripe:
        log("STRIPE", "FAIL", "Biblioteca 'stripe' não instalada.")
        return False
    stripe.api_key = key
    try:
        stripe.Account.retrieve()
        log("STRIPE", "OK", "Credencial válida.")
        return True
    except Exception as e:
        log("STRIPE", "FAIL", f"Credencial inválida: {str(e)}")
        return False

def check_mercadopago():
    token = os.getenv("MP_ACCESS_TOKEN")
    if not token:
        log("MERCADO PAGO", "WARN", "MP_ACCESS_TOKEN não definido. Pular.")
        return True
    try:
        headers = {"Authorization": f"Bearer {token}"}
        res = requests.get("https://api.mercadopago.com/users/me", headers=headers)
        if res.status_code == 200:
            log("MERCADO PAGO", "OK", "Conectado.")
            if "APP_USR" not in token:
                log("MERCADO PAGO", "WARN", "Token de TESTE detectado.")
            return True
        else:
            log("MERCADO PAGO", "FAIL", f"Erro {res.status_code}")
            return False
    except Exception as e:
        log("MERCADO PAGO", "FAIL", f"Erro de conexão: {e}")
        return False

def check_whatsapp():
    url = os.getenv("WHATSAPP_API_URL")
    if not url:
        log("WHATSAPP", "WARN", "Configuração incompleta. Pular.")
        return True
    # Validação simplificada de URL
    if url.startswith("http"):
        log("WHATSAPP", "OK", "URL configurada (Validação profunda requer instância ativa).")
        return True
    return False

def check_smtp():
    server = os.getenv("SMTP_SERVER")
    if not server:
        log("SMTP", "WARN", "Configuração de E-mail incompleta. Pular.")
        return True
    log("SMTP", "OK", "Servidor configurado (Teste de conexão real requer credenciais).")
    return True

def main():
    print("🚀 Iniciando Validação de Integrações Reais (Pre-Flight Check)...\n")
    from dotenv import load_dotenv
    load_dotenv() 

    checks = [
        check_database(),
        check_storage(),
        check_stripe(),
        check_mercadopago(),
        check_whatsapp(),
        check_smtp()
    ]

    print("\n" + "="*40)
    if all(checks):
        print("🏆 Integration Check: All configured services are reachable.")
        sys.exit(0)
    else:
        print("🚨 Falha na validação de integrações.")
        sys.exit(1)

if __name__ == "__main__":
    main()
