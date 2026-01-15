import os
import re
from pathlib import Path

def fix_app_gradle():
    print("🔧 Injetando NDK 26.1.10909125 no app/build.gradle...")
    
    root_dir = Path.cwd()
    app_gradle = root_dir / "mobile" / "android" / "app" / "build.gradle"
    
    if not app_gradle.exists():
        print("❌ Arquivo app/build.gradle não encontrado.")
        return

    try:
        with open(app_gradle, "r", encoding="utf-8") as f:
            content = f.read()

        # Verifica se já tem a versão correta
        if 'ndkVersion "26.1.10909125"' in content:
            print("✅ app/build.gradle já está configurado corretamente.")
            return

        # Se tiver outra versão, substitui
        if "ndkVersion" in content:
            print("   Substituindo versão antiga...")
            new_content = re.sub(
                r'ndkVersion\s+["\'].*["\']', 
                'ndkVersion "26.1.10909125"', 
                content
            )
        else:
            # Se não tiver, insere logo após 'android {'
            print("   Inserindo configuração ndkVersion...")
            new_content = re.sub(
                r'android\s*\{', 
                'android {\n    ndkVersion "26.1.10909125"', 
                content,
                count=1
            )

        with open(app_gradle, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        print("✅ Sucesso! Configuração aplicada no módulo do app.")

    except Exception as e:
        print(f"❌ Erro ao editar arquivo: {e}")

if __name__ == "__main__":
    fix_app_gradle()
