import os
import sys

def verify():
    print("🔍 Verificando TASK-000: Inventário Técnico...")

    target_file = "docs/audit/REPO_INVENTORY.md"

    # 1. Verificação de Existência
    if not os.path.exists(target_file):
        print(f"❌ Arquivo {target_file} não encontrado.")
        sys.exit(1)

    # 2. Verificação de Conteúdo Mínimo
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()
        
        required_sections = [
            "Backend", "Frontend", "Mobile", 
            "app/services", "app/routers", 
            "src/app", "src/lib", 
            "mobile/src", 
            "scripts/setup", "scripts/maintenance"
        ]

        missing = []
        for term in required_sections:
            if term not in content:
                missing.append(term)

        if missing:
            print(f"❌ Conteúdo incompleto. Faltando seções: {missing}")
            sys.exit(1)

    print(f"✅ Inventário gerado com sucesso em {target_file}.")
    sys.exit(0)

if __name__ == "__main__":
    verify()