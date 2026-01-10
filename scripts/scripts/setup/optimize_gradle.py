import os
from pathlib import Path

def optimize_gradle():
    print("🚀 Otimizando configurações do Gradle para Alta Performance...")
    
    root_dir = Path.cwd()
    gradle_props = root_dir / "mobile" / "android" / "gradle.properties"
    
    if not gradle_props.exists():
        print("❌ Arquivo gradle.properties não encontrado.")
        print("   Execute 'npx expo prebuild' primeiro.")
        return

    # Configurações de "Turbo Mode"
    # -Xmx4096m: Dá 4GB de RAM para o compilador (padrão é 2GB ou menos)
    # parallel: Compila módulos ao mesmo tempo
    # daemon: Mantém o Java vivo na memória para o próximo build ser instantâneo
    optimizations = """
# --- MESAFLOW TURBO BUILD ---
org.gradle.jvmargs=-Xmx4096m -XX:MaxMetaspaceSize=1024m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8
org.gradle.daemon=true
org.gradle.parallel=true
org.gradle.configureondemand=true
org.gradle.caching=true
android.useAndroidX=true
android.enableJetifier=true
# ----------------------------
"""

    try:
        # Lê o conteúdo atual
        with open(gradle_props, "r", encoding="utf-8") as f:
            content = f.read()

        # Se já estiver otimizado, avisa
        if "MESAFLOW TURBO BUILD" in content:
            print("✅ O Gradle já está otimizado.")
            return

        # Adiciona as otimizações no final
        with open(gradle_props, "a", encoding="utf-8") as f:
            f.write("\n" + optimizations)
            
        print("✅ Configurações aplicadas com sucesso!")
        print("   - Memória Heap aumentada para 4GB")
        print("   - Compilação paralela ativada")
        print("   - Cache de build ativado")
        
    except Exception as e:
        print(f"❌ Erro ao otimizar: {e}")

if __name__ == "__main__":
    optimize_gradle()
