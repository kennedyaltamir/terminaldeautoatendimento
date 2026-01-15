import os
import sys
from pathlib import Path

def fix_sdk_location():
    print("🔧 Configurando Android SDK...")

    # 1. Tenta encontrar o SDK automaticamente no Windows
    user_home = Path.home()
    possible_paths = [
        user_home / "AppData" / "Local" / "Android" / "Sdk",
        Path("C:/Android/Sdk"),
        Path("C:/Program Files (x86)/Android/android-sdk"),
    ]

    sdk_path = None
    for p in possible_paths:
        if p.exists():
            sdk_path = p
            break

    # 2. Se não achar, pede pro usuário (ou usa variável de ambiente)
    if not sdk_path:
        env_home = os.environ.get("ANDROID_HOME")
        if env_home and Path(env_home).exists():
            sdk_path = Path(env_home)
        else:
            print("❌ Não foi possível encontrar o Android SDK automaticamente.")
            print("   Por favor, verifique se o Android Studio está instalado.")
            print("   Caminho padrão esperado: %LOCALAPPDATA%\\Android\\Sdk")
            return

    print(f"✅ SDK Encontrado: {sdk_path}")

    # 3. Formata o caminho para o padrão do local.properties (escapando barras)
    # No Windows, o arquivo espera C\:\\Users\\... ou C:/Users/...
    # Vamos usar barras normais (/) que funcionam bem no Java/Gradle
    sdk_str = str(sdk_path).replace("\\", "/")

    # 4. Escreve no arquivo local.properties
    project_root = Path.cwd()
    android_dir = project_root / "mobile" / "android"
    
    if not android_dir.exists():
        print("❌ Pasta mobile/android não encontrada. Rode 'npx expo prebuild' primeiro.")
        return

    prop_file = android_dir / "local.properties"
    
    content = f"sdk.dir={sdk_str}\n"
    
    try:
        with open(prop_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Arquivo criado com sucesso: {prop_file}")
        print(f"   Conteúdo: {content.strip()}")
        print("\n🚀 Agora você pode tentar o build novamente!")
    except Exception as e:
        print(f"❌ Erro ao escrever arquivo: {e}")

if __name__ == "__main__":
    fix_sdk_location()
