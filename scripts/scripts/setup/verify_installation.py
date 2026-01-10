import os
import sys
import importlib.util
import io

# Força UTF-8 no Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_file(path):
    if os.path.exists(path):
        print(f"✅ Encontrado: {path}")
        return True
    else:
        print(f"❌ FALTANDO: {path}")
        return False

def check_dependency(package_name):
    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        print(f"✅ Dependência Python: {package_name}")
    else:
        print(f"❌ Dependência Python FALTANDO: {package_name}")

def main():
    print("🔍 Iniciando Verificação de Integridade do MesaFlow...\n")

    # 1. Arquivos Críticos do Backend
    backend_files = [
        "app/main.py",
        "app/models.py",
        "app/schemas.py",
        "app/database.py",
        "app/services/payment_service.py",
        "app/services/stock_service.py",
        "app/core/limiter.py",
    ]
    
    # 2. Arquivos Críticos do Frontend
    frontend_files = [
        "frontend/package.json",
        "frontend/next.config.mjs",
        "frontend/src/app/page.tsx",
        "frontend/src/app/admin/login/page.tsx",
        "frontend/src/app/admin/[slug]/settings/page.tsx",
        "frontend/src/app/admin/[slug]/inventory/page.tsx",
        "frontend/src/lib/validations/settings.ts",
        "frontend/src/lib/validations/auth.ts",
        "frontend/src/components/ui/ColorPicker.tsx",
    ]

    all_ok = True

    print("--- Backend ---")
    for f in backend_files:
        if not check_file(f): all_ok = False
        
    print("\n--- Frontend ---")
    for f in frontend_files:
        if not check_file(f): all_ok = False

    print("\n--- Dependências Python Críticas ---")
    py_deps = ["fastapi", "sqlalchemy", "slowapi", "httpx"]
    for d in py_deps:
        check_dependency(d)

    print("\n" + "="*40)
    if all_ok:
        print("🎉 TUDO PRONTO! O sistema está íntegro.")
        print("👉 Para rodar: python run.py")
    else:
        print("⚠️  Alguns arquivos estão faltando. Verifique o log acima.")
    print("="*40)

if __name__ == "__main__":
    main()
