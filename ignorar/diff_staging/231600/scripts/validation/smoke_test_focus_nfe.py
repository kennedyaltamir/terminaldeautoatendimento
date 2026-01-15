# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 23:15:00
import os
import sys
import io
import httpx
from dotenv import load_dotenv

# Windows Resilience
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def run_smoke_test():
    load_dotenv(override=True)
    
    token = os.getenv("FISCAL_TOKEN")
    env = os.getenv("FISCAL_ENV", "sandbox")
    
    print(f"🚀 Iniciando Smoke Test: Focus NFe ({env})")
    
    if not token:
        print("❌ ERRO: FISCAL_TOKEN não encontrado no .env")
        return 1
        
    base_url = "https://homologacao.focusnfe.com.br/v2" if env == "sandbox" else "https://api.focusnfe.com.br/v2"
    
    # Focus NFe utiliza Basic Auth: (Token, "")
    auth = (token, "")
    
    print(f"📡 Verificando autenticação no endpoint /v2/hooks...")
    
    try:
        with httpx.Client(timeout=10.0) as client:
            # Hooks é um endpoint leve para testar a credencial
            response = client.get(f"{base_url}/hooks", auth=auth)
            
            if response.status_code == 200:
                print("✅ SUCESSO: Token válido e comunicação estabelecida!")
                return 0
            elif response.status_code == 401:
                print("❌ FALHA: Token inválido (401 Unauthorized).")
                return 1
            else:
                print(f"⚠️  RESPOSTA INESPERADA: {response.status_code}")
                print(f"Conteúdo: {response.text[:200]}")
                return 1
                
    except Exception as e:
        print(f"💥 ERRO DE CONEXÃO: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(run_smoke_test())
