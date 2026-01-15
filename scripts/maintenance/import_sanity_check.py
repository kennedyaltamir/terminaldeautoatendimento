
import sys
import os

# Adiciona a raiz ao path
sys.path.append(os.getcwd())

def test_imports():
    print("🔍 Verificando Integridade de Importações (Pós-Modularização)...")
    errors = 0
    
    modules_to_test = [
        "app.models",
        "app.models.core",
        "app.models.auth",
        "app.models.menu",
        "app.models.orders",
        "app.models.fintech",
        "app.models.public",
        "app.schemas",
        "app.schemas.core",
        "app.schemas.auth",
        "app.schemas.menu",
        "app.schemas.orders",
        "app.schemas.company",
        "app.schemas.fintech",
        "app.schemas.public"
    ]

    for module in modules_to_test:
        try:
            __import__(module)
            print(f"   ✅ {module:<25} | OK")
        except ImportError as e:
            print(f"   ❌ {module:<25} | FALHA: {e}")
            errors += 1
        except Exception as e:
            print(f"   ❌ {module:<25} | ERRO INESPERADO: {e}")
            errors += 1

    if errors == 0:
        print("\n✨ Todas as importações core estão íntegras.")
        return True
    else:
        print(f"\n🚨 Detectados {errors} erros de importação. Verifique os arquivos __init__.py.")
        return False

if __name__ == "__main__":
    if not test_imports():
        sys.exit(1)

