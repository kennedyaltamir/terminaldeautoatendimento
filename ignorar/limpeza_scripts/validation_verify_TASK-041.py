import sys
import os
import json

def verify():
    print("🔍 Verificando TASK-041: Otimização com FlashList...")
    
    # 1. Verificação de Arquivos
    required_files = [
        "mobile/src/screens/orders/OrdersScreen.tsx",
        "mobile/package.json"
    ]
    
    for f_path in required_files:
        if not os.path.exists(f_path):
            print(f"❌ Arquivo faltando: {f_path}")
            sys.exit(1)
        print(f"✅ Arquivo encontrado: {f_path}")

    # 2. Validação de package.json (Dependência)
    try:
        with open("mobile/package.json", "r", encoding="utf-8") as f:
            pkg = json.load(f)
            if "@shopify/flash-list" not in pkg.get("dependencies", {}):
                print("❌ Dependência '@shopify/flash-list' não encontrada no package.json.")
                print("   👉 Execute: python scripts/setup/install_flashlist.py")
                sys.exit(1)
            print("✅ Dependência '@shopify/flash-list' confirmada.")
    except Exception as e:
        print(f"❌ Erro ao ler package.json: {e}")
        sys.exit(1)

    # 3. Validação de Código (OrdersScreen)
    with open("mobile/src/screens/orders/OrdersScreen.tsx", "r", encoding="utf-8") as f:
        content = f.read()
        
        if "import { FlashList } from '@shopify/flash-list'" not in content:
            print("❌ Importação do FlashList ausente em OrdersScreen.tsx")
            sys.exit(1)
            
        if "<FlashList" not in content:
            print("❌ Componente FlashList não utilizado no JSX.")
            sys.exit(1)
            
        if "estimatedItemSize=" not in content:
            print("❌ Propriedade 'estimatedItemSize' obrigatória não encontrada.")
            sys.exit(1)
            
        if "FlatList" in content and "import { FlatList" in content:
             print("⚠️  Aviso: FlatList ainda está sendo importado. Verifique se é necessário.")

    print("\n🏆 TASK-041: OTIMIZAÇÃO FLASHLIST VALIDADA COM SUCESSO.")
    sys.exit(0)

if __name__ == "__main__":
    verify()
