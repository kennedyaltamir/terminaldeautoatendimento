import os
import sys
import re

def verify():
    print("🔍 Verificando Auth Boundary e Root Exclusivity (v2.2)...")

    errors = 0
    
    # 1. Verificar exclusividade no RootNavigator
    root_nav_path = "mobile/src/navigation/RootNavigator.tsx"
    if os.path.exists(root_nav_path):
        with open(root_nav_path, "r", encoding="utf-8") as f:
            content = f.read()
            
            # Garante que renderiza AuthGate
            if "return <AuthGate />" not in content:
                print("❌ VIOLAÇÃO: RootNavigator deve renderizar exclusivamente <AuthGate />.")
                errors += 1
            
            # Garante que NÃO renderiza stacks diretamente (vazamento de decisão)
            if "<AppStack" in content or "<AuthStack" in content:
                print("❌ VIOLAÇÃO: RootNavigator está renderizando Stacks diretamente.")
                errors += 1
            else:
                print("✅ RootNavigator exclusividade validada.")

    # 2. Verificar lógica do AuthGate (Regex resiliente a quebras de linha e espaços)
    gate_path = "mobile/src/navigation/AuthGate.tsx"
    if os.path.exists(gate_path):
        with open(gate_path, "r", encoding="utf-8") as f:
            content = f.read()
            
            checks = [
                (r"case\s+'idle':.*?case\s+'hydrating':.*?case\s+'checking_expiry':.*?return\s+null", 
                 "Estados de transição retornam null"),
                (r"case\s+'authenticated':.*?return\s+<AppStack\s+/>", 
                 "Estado autenticado renderiza AppStack"),
                (r"case\s+'unauthenticated':.*?case\s+'error':.*?return\s+<AuthStack\s+/>", 
                 "Estado não autenticado/erro renderiza AuthStack")
            ]
            
            for pattern, desc in checks:
                # O uso de re.S (DOTALL) permite que o '.' capture quebras de linha
                if re.search(pattern, content, re.S):
                    print(f"✅ Lógica do Gate: {desc} - OK")
                else:
                    print(f"❌ Lógica do Gate: {desc} - FALHA")
                    errors += 1

    # 3. Verificar existência da Auditoria JWT
    audit_path = "docs/mobile/decisions/JWT_BACKEND_AUDIT.md"
    if not os.path.exists(audit_path):
        print("❌ FALTANDO: Evidência de Auditoria JWT Backend.")
        errors += 1
    else:
        print("✅ Auditoria JWT Backend encontrada.")

    if errors > 0:
        print(f"\n🚨 Falha na validação: {errors} erro(s).")
        sys.exit(1)

    print("\n✨ Mobile Auth Boundary & Exclusivity verified successfully.")

if __name__ == "__main__":
    verify()
