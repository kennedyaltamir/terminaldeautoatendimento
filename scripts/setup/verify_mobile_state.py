import os
import sys
import json

def verify():
    print("🔍 Verificando Gestão de Estado Mobile (Zustand)...")
    
    # 1. Verificar dependência no package.json
    pkg_path = "mobile/package.json"
    if not os.path.exists(pkg_path):
        print("❌ Erro: mobile/package.json não encontrado.")
        sys.exit(1)
        
    with open(pkg_path, "r") as f:
        pkg = json.load(f)
        if "zustand" not in pkg.get("dependencies", {}):
            print("❌ Erro: Dependência 'zustand' não encontrada no package.json.")
            sys.exit(1)
    
    # 2. Verificar arquivos críticos
    checks = [
        ("mobile/src/types/auth.types.ts", "AuthStatus"),
        ("mobile/src/store/auth.store.ts", "useAuthStore"),
        ("docs/mobile/decisions/MISSION_GOVERNANCE.md", "BLOCKER"),
        ("docs/mobile/tasks/mobile_12_auth_application.md", "Lifecycle")
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

    # 3. Validação de Escopo Negativo (Proibido UI)
    print("🛡️ Verificando violação de escopo (UI/TSX)...")
    forbidden_dirs = ["mobile/src/screens", "mobile/src/components"]
    for d in forbidden_dirs:
        if os.path.exists(d):
            files = [f for f in os.listdir(d) if f.endswith(".tsx")]
            if files:
                print(f"❌ VIOLAÇÃO DE ESCOPO: Arquivos de UI encontrados em {d}: {files}")
                errors += 1

    if errors > 0:
        print(f"\n🚨 Falha na validação: {errors} erro(s) encontrado(s).")
        sys.exit(1)
    
    print("\n✨ Mobile State Management verified successfully.")

if __name__ == "__main__":
    verify()
