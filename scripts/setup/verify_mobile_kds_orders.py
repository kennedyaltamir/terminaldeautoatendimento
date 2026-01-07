import os
import sys

def verify():
    print("🔍 Verificando Módulo KDS Orders Mobile...")

    critical_files = [
        "mobile/src/services/orders.service.ts",
        "mobile/src/store/orders.store.ts",
        "mobile/src/screens/orders/OrdersScreen.tsx",
        "docs/mobile/tasks/mobile_17_kds_orders.md"
    ]

    errors = 0
    for f in critical_files:
        if not os.path.exists(f):
            print(f"❌ Arquivo ausente: {f}")
            errors += 1
        else:
            print(f"✅ Encontrado: {f}")

    # Validação de uso de UI Foundation e Tokens
    screen_path = "mobile/src/screens/orders/OrdersScreen.tsx"
    if os.path.exists(screen_path):
        with open(screen_path, "r", encoding="utf-8") as f:
            content = f.read()
            
            # Verifica se importa componentes da UI Foundation
            if "ui/components/Card" not in content or "ui/components/Button" not in content:
                print(f"❌ VIOLAÇÃO: OrdersScreen deve usar componentes da UI Foundation.")
                errors += 1
            
            # Verifica se usa tokens de cor (não hexadecimais)
            if "#" in content and "colors." not in content:
                # Permite '#' apenas se for parte de um comentário ou string permitida, 
                # mas aqui buscamos por valores hardcoded no StyleSheet.
                if "backgroundColor: '#" in content or "color: '#" in content:
                    print(f"❌ VIOLAÇÃO: Cores hardcoded encontradas em {screen_path}. Use colors.ts.")
                    errors += 1
            
            # Verifica se usa tokens de espaçamento
            if "spacing." not in content:
                print(f"❌ VIOLAÇÃO: Espaçamentos hardcoded encontrados em {screen_path}. Use spacing.ts.")
                errors += 1

    if errors > 0:
        print(f"\n🚨 Falha na validação: {errors} erro(s).")
        sys.exit(1)

    print("\n✨ Mobile KDS Orders module verified successfully.")

if __name__ == "__main__":
    verify()
