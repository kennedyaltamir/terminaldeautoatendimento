import os
import sys
import json

def verify():
    print("🔍 Verificando Autenticação Semântica Mobile (v2.0)...")

    # 1. Verificar Dependência
    pkg_path = "mobile/package.json"
    if not os.path.exists(pkg_path):
        print("❌ Erro: mobile/package.json não encontrado.")
        sys.exit(1)

    with open(pkg_path, "r") as f:
        pkg = json.load(f)
        if "jwt-decode" not in pkg.get("dependencies", {}):
            print("❌ Erro: Dependência 'jwt-decode' ausente.")
            sys.exit(1)

    # 2. Verificar Inexistência de Escopo Fantasma (UX em Auth)
    auth_store_path = "mobile/src/store/auth.store.ts"
    with open(auth_store_path, "r", encoding="utf-8") as f:
        content = f.read()
        forbidden = ["userName", "companyName", "companySlug"]
        for word in forbidden:
            if word in content:
                print(f"❌ VIOLAÇÃO DE ESCOPO: '{word}' encontrado em {auth_store_path}")
                sys.exit(1)

    # 3. Verificar Estados Observáveis
    auth_types_path = "mobile/src/types/auth.types.ts"
    with open(auth_types_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "'checking_expiry'" not in content:
            print(f"❌ ERRO: Estado 'checking_expiry' não definido em {auth_types_path}")
            sys.exit(1)

    # 4. Verificar Constante de Buffer
    jwt_service_path = "mobile/src/services/auth/jwt.ts"
    with open(jwt_service_path, "r", encoding="utf-8") as f:
        if "EXPIRY_GRACE_SECONDS" not in f.read():
            print(f"❌ ERRO: Constante 'EXPIRY_GRACE_SECONDS' ausente em {jwt_service_path}")
            sys.exit(1)

    print("\n✨ Mobile Semantic Auth verified successfully (Strict Compliance).")

if __name__ == "__main__":
    verify()
