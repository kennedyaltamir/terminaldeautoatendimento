import os
import sys
import subprocess
import re
from pathlib import Path

# Configuração
REQUIRED_NDK_VERSION = "26.1.10909125"
REQUIRED_CMAKE_VERSION = "3.22.1"

def get_sdk_path():
    """Lê o caminho do SDK do local.properties ou tenta adivinhar."""
    root_dir = Path.cwd()
    local_props = root_dir / "mobile" / "android" / "local.properties"
    
    if local_props.exists():
        with open(local_props, "r") as f:
            for line in f:
                if line.strip().startswith("sdk.dir"):
                    path_str = line.split("=")[1].strip()
                    # Corrige formato Windows (C\:\\Users...)
                    path_str = path_str.replace("\\:", ":").replace("\\\\", "\\")
                    return Path(path_str)
    
    # Fallback padrão Windows
    return Path(os.environ["LOCALAPPDATA"]) / "Android" / "Sdk"

def find_sdkmanager(sdk_path):
    """Busca recursiva pelo sdkmanager.bat."""
    print("🔍 Procurando sdkmanager...")
    for path in sdk_path.rglob("sdkmanager.bat"):
        return path
    return None

def install_components(sdk_path):
    """Instala NDK e CMake específicos."""
    sdkmanager = find_sdkmanager(sdk_path)
    if not sdkmanager:
        print("❌ 'sdkmanager' não encontrado. Instale 'Android SDK Command-line Tools' via Android Studio.")
        return False

    packages = [
        f"ndk;{REQUIRED_NDK_VERSION}",
        f"cmake;{REQUIRED_CMAKE_VERSION}"
    ]
    
    print(f"⬇️  Instalando dependências nativas: {', '.join(packages)}...")
    cmd = f'echo y | "{str(sdkmanager)}" --install ' + " ".join([f'"{p}"' for p in packages])
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print("✅ Componentes instalados.")
        return True
    except subprocess.CalledProcessError:
        print("❌ Falha na instalação automática.")
        return False

def patch_build_gradle():
    """Força a versão do NDK no build.gradle."""
    gradle_file = Path.cwd() / "mobile" / "android" / "build.gradle"
    if not gradle_file.exists():
        print("❌ build.gradle não encontrado.")
        return

    print("🔧 Patcheando build.gradle...")
    content = gradle_file.read_text(encoding="utf-8")

    # Regex para encontrar o bloco buildscript { ext { ... } }
    # Procura por 'buildscript {' seguido de qualquer coisa até 'ext {'
    pattern = re.compile(r'(buildscript\s*\{[\s\S]*?ext\s*\{)', re.MULTILINE)
    
    if pattern.search(content):
        # Verifica se já tem ndkVersion
        if "ndkVersion" in content:
            # Substitui a versão existente
            new_content = re.sub(r'ndkVersion\s*=\s*".*"', f'ndkVersion = "{REQUIRED_NDK_VERSION}"', content)
        else:
            # Insere a versão logo após 'ext {'
            new_content = pattern.sub(f'\\1\n        ndkVersion = "{REQUIRED_NDK_VERSION}"', content)
        
        gradle_file.write_text(new_content, encoding="utf-8")
        print(f"✅ ndkVersion definido para {REQUIRED_NDK_VERSION}")
    else:
        print("⚠️  Estrutura do build.gradle não reconhecida. Tentando append manual...")
        # Fallback: Adiciona no final do arquivo (pode não funcionar dependendo da estrutura)
        # Mas em projetos Expo, o ext costuma estar no topo.
        pass

def patch_local_properties(sdk_path):
    """Adiciona ndk.dir ao local.properties."""
    props_file = Path.cwd() / "mobile" / "android" / "local.properties"
    ndk_path = sdk_path / "ndk" / REQUIRED_NDK_VERSION
    
    if not ndk_path.exists():
        print(f"❌ NDK {REQUIRED_NDK_VERSION} não encontrado em {ndk_path}")
        return

    print("🔧 Atualizando local.properties...")
    
    # Formato seguro para Windows (escapando barras)
    ndk_str = str(ndk_path).replace("\\", "\\\\").replace(":", "\\:")
    sdk_str = str(sdk_path).replace("\\", "\\\\").replace(":", "\\:")
    
    content = f"sdk.dir={sdk_str}\nndk.dir={ndk_str}\n"
    
    props_file.write_text(content, encoding="utf-8")
    print("✅ local.properties atualizado com caminho explícito do NDK.")

def main():
    print("🚀 Iniciando Correção de Ambiente de Build...")
    
    sdk_path = get_sdk_path()
    if not sdk_path.exists():
        print(f"❌ SDK não encontrado em {sdk_path}")
        return

    # 1. Verificar se NDK existe
    ndk_path = sdk_path / "ndk" / REQUIRED_NDK_VERSION
    if not ndk_path.exists():
        print(f"⚠️  NDK {REQUIRED_NDK_VERSION} ausente.")
        if not install_components(sdk_path):
            print("\n🚨 AÇÃO MANUAL NECESSÁRIA:")
            print("1. Abra o Android Studio.")
            print("2. Vá em Tools > SDK Manager > SDK Tools.")
            print("3. Marque 'Show Package Details'.")
            print(f"4. Expanda 'NDK (Side by side)' e marque '{REQUIRED_NDK_VERSION}'.")
            print(f"5. Expanda 'CMake' e marque '{REQUIRED_CMAKE_VERSION}'.")
            print("6. Clique em Apply.")
            return
    else:
        print(f"✅ NDK {REQUIRED_NDK_VERSION} detectado.")

    # 2. Aplicar Patches
    patch_build_gradle()
    patch_local_properties(sdk_path)

    print("\n✨ Ambiente corrigido! Tente rodar o build novamente.")

if __name__ == "__main__":
    main()
