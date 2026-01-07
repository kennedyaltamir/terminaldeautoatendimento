import os
import sys
import re

def verify():
    print("🔍 Verificando UI Foundation Mobile (v1.0)...")

    critical_files = [
        "mobile/src/ui/tokens/colors.ts",
        "mobile/src/ui/tokens/spacing.ts",
        "mobile/src/ui/tokens/typography.ts",
        "mobile/src/ui/components/Button.tsx",
        "mobile/src/ui/components/Input.tsx",
        "mobile/src/ui/components/Card.tsx",
        "docs/mobile/tasks/mobile_15_ui_foundation.md"
    ]

    errors = 0
    for f in critical_files:
        if not os.path.exists(f):
            print(f"❌ Arquivo ausente: {f}")
            errors += 1
        else:
            print(f"✅ Encontrado: {f}")

    # Validação de "Pure UI" (Proibição de acoplamento com lógica de negócio)
    components_dir = "mobile/src/ui/components"
    forbidden_terms = ["useAuthStore", "navigation", "AuthGate", "api", "axios"]
    
    if os.path.exists(components_dir):
        for file in os.listdir(components_dir):
            if file.endswith(".tsx"):
                path = os.path.join(components_dir, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    for term in forbidden_terms:
                        if term in content:
                            print(f"❌ VIOLAÇÃO DE PURE UI: Termo '{term}' encontrado em {path}")
                            errors += 1

    # Validação de Hardcoded Colors (Exceto no arquivo de tokens)
    print("🛡️ Verificando uso estrito de tokens...")
    hex_pattern = r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})'
    for file in os.listdir(components_dir):
        if file.endswith(".tsx"):
            path = os.path.join(components_dir, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                if re.search(hex_pattern, content):
                    print(f"❌ VIOLAÇÃO: Valor hexadecimal hardcoded encontrado em {path}. Use tokens/colors.ts.")
                    errors += 1

    if errors > 0:
        print(f"\n🚨 Falha na validação: {errors} erro(s).")
        sys.exit(1)

    print("\n✨ Mobile UI Foundation verified successfully.")

if __name__ == "__main__":
    verify()
