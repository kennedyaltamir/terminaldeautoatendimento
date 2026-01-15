import os
import re
from pathlib import Path

def force_ndk_gradle():
    print("🔧 Forçando NDK 26.1.10909125 no build.gradle...")
    
    root_dir = Path.cwd()
    gradle_file = root_dir / "mobile" / "android" / "build.gradle"
    
    if not gradle_file.exists():
        print("❌ Arquivo build.gradle não encontrado.")
        return

    try:
        with open(gradle_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Estratégia 1: Se já existe ndkVersion, substitui
        if "ndkVersion" in content:
            print("   Encontrado ndkVersion existente. Substituindo...")
            new_content = re.sub(
                r'ndkVersion\s*=\s*".*"', 
                'ndkVersion = "26.1.10909125"', 
                content
            )
        
        # Estratégia 2: Se não existe, injeta no bloco ext
        elif "ext {" in content:
            print("   ndkVersion não encontrado. Injetando no bloco ext...")
            new_content = content.replace(
                "ext {", 
                'ext {\n        ndkVersion = "26.1.10909125"', 
                1
            )
        
        else:
            print("❌ Não foi possível encontrar um local seguro para injetar a versão.")
            return

        with open(gradle_file, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        print("✅ build.gradle atualizado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {e}")

def verify_local_properties():
    print("\n🔧 Verificando local.properties...")
    root_dir = Path.cwd()
    props_file = root_dir / "mobile" / "android" / "local.properties"
    
    if props_file.exists():
        with open(props_file, "r", encoding="utf-8") as f:
            content = f.read()
            if "26.1.10909125" in content:
                print("✅ local.properties já aponta para o NDK 26.")
            else:
                print("⚠️  local.properties pode estar apontando para versão errada.")
                # O script anterior já deve ter ajustado isso, mas é bom avisar

if __name__ == "__main__":
    force_ndk_gradle()
    verify_local_properties()
