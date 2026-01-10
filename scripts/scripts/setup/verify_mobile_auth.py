import os
import sys

def verify():
    print("🔍 Verificando Infraestrutura de Autenticação Mobile...")
    
    checks = [
        ("mobile/src/services/auth/storage.ts", "AuthStoragePort"),
        ("mobile/src/services/api.ts", "interceptors.response.use"),
        ("mobile/src/services/auth/client.ts", "AuthClient"),
        ("mobile/src/types/auth.ts", "RefreshTokenError")
    ]
    
    errors = 0
    for path, content in checks:
        if not os.path.exists(path):
            print(f"❌ Arquivo ausente: {path}")
            errors += 1
            continue
            
        with open(path, "r", encoding="utf-8") as f:
            if content not in f.read():
                print(f"❌ Conteúdo obrigatório '{content}' não encontrado em {path}")
                errors += 1
            else:
                print(f"✅ {path} validado.")

    if errors > 0:
        print(f"\n🚨 Falha na validação: {errors} erro(s) encontrado(s).")
        sys.exit(1)
    
    print("\n✨ Mobile Auth Infrastructure verified successfully.")

if __name__ == "__main__":
    verify()
