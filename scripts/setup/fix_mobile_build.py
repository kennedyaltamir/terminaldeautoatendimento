import os
import sys
from pathlib import Path

# [TEST_EXEMPT: Script de infraestrutura para correção de ambiente local]

def fix_mobile_infrastructure():
    print("🚀 Iniciando reparo atômico do ambiente nativo MesaFlow...")

    # 1. Definição de Caminhos
    base_path = Path("C:/mesaflow/mobile/android")
    gradle_props_path = base_path / "gradle.properties"
    local_props_path = base_path / "local.properties"
    
    # Caminhos de Sistema detectados nos logs anteriores
    android_sdk_path = "C:\\Android\\Sdk"
    java_home_path = "C:\\Program Files\\Android\\Android Studio\\jbr"

    if not base_path.exists():
        print(f"❌ Erro: Pasta nativa não encontrada em {base_path}")
        print("Execute 'npx expo prebuild' dentro da pasta mobile primeiro.")
        return

    # 2. Conteúdo para gradle.properties (Memória + Hermes + New Arch)
    # Estas flags são obrigatórias para o build não quebrar na linha 177
    gradle_content = [
        "# Configurações de Memória (Fix Kotlin Internal Compiler Error)",
        "org.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=512m",
        "org.gradle.daemon=true",
        "org.gradle.parallel=true",
        "org.gradle.configureondemand=true",
        "",
        "# Configurações de Engine (Fix hermesEnabled Error)",
        "hermesEnabled=true",
        "newArchEnabled=true",
        "",
        "# Expo Specifics",
        "expo.webp.animated=true",
        "expo.webp.isWebpSupportEnabled=true"
    ]

    # 3. Conteúdo para local.properties
    local_content = [
        f"sdk.dir={android_sdk_path.replace('\\', '/')}",
        f"java.home={java_home_path.replace('\\', '/')}"
    ]

    try:
        # Escrita do gradle.properties
        with open(gradle_props_path, "w", encoding="utf-8") as f:
            f.write("\n".join(gradle_content))
        print(f"✅ {gradle_props_path} atualizado com flags do Hermes.")

        # Escrita do local.properties
        with open(local_props_path, "w", encoding="utf-8") as f:
            f.write("\n".join(local_content))
        print(f"✅ {local_props_path} atualizado com caminhos do SDK.")

        print("\n✨ Ambiente sincronizado com sucesso!")
        print("👉 Próximos passos:")
        print(f"   1. cd mobile")
        print(f"   2. $env:JAVA_HOME = \"{java_home_path}\"")
        print(f"   3. npx expo run:android")

    except Exception as e:
        print(f"💥 Falha ao gravar arquivos de configuração: {e}")

if __name__ == "__main__":
    fix_mobile_infrastructure()
