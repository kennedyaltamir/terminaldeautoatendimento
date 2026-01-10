import sys
import os

def verify():
    print("🔍 Verificando TASK-042: Automação de Store...")
    
    # 1. Verificação de Arquivos Fastlane
    required_files = [
        "mobile/fastlane/Fastfile",
        "mobile/fastlane/Snapfile",
        "scripts/automation/capture_mobile_screens.py"
    ]
    
    for f_path in required_files:
        if not os.path.exists(f_path):
            print(f"❌ Arquivo faltando: {f_path}")
            sys.exit(1)
        print(f"✅ Arquivo encontrado: {f_path}")

    # 2. Verificação de Conteúdo do Fastfile
    with open("mobile/fastlane/Fastfile", "r", encoding="utf-8") as f:
        content = f.read()
        if "lane :screenshots" not in content:
            print("❌ Lane 'screenshots' não encontrada no Fastfile.")
            sys.exit(1)
        if "capture_mobile_screens.py" not in content:
            print("❌ Chamada ao script Python ausente no Fastfile.")
            sys.exit(1)

    # 3. Verificação do Script de Automação
    with open("scripts/automation/capture_mobile_screens.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "adb shell screencap" not in content:
            print("❌ Comando de captura ADB ausente no script.")
            sys.exit(1)

    print("\n🏆 TASK-042: INFRAESTRUTURA DE AUTOMAÇÃO VALIDADA.")
    sys.exit(0)

if __name__ == "__main__":
    verify()
