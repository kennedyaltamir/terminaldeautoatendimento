import os
from pathlib import Path

def force_ndk():
    print("🔧 Forçando versão do NDK para 26.1.10909125...")
    
    root_dir = Path.cwd()
    build_gradle = root_dir / "mobile" / "android" / "build.gradle"
    
    if not build_gradle.exists():
        print("❌ Arquivo build.gradle não encontrado. Rode 'npx expo prebuild' primeiro.")
        return

    try:
        with open(build_gradle, "r", encoding="utf-8") as f:
            content = f.read()

        # Verifica se já está configurado
        if 'ndkVersion = "26.1.10909125"' in content:
            print("✅ NDK já está configurado corretamente.")
            return

        # Injeta a versão no bloco ext ou buildscript
        # A estratégia mais segura é adicionar no bloco ext { ... } que o Expo gera
        if "ext {" in content:
            new_content = content.replace("ext {", 'ext {\n        ndkVersion = "26.1.10909125"', 1)
            
            with open(build_gradle, "w", encoding="utf-8") as f:
                f.write(new_content)
                
            print("✅ Configuração injetada com sucesso!")
            print("   ndkVersion = \"26.1.10909125\"")
        else:
            print("⚠️  Não foi possível localizar o bloco 'ext {'. A injeção falhou.")

    except Exception as e:
        print(f"❌ Erro ao editar arquivo: {e}")

if __name__ == "__main__":
    force_ndk()
