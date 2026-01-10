import os
import subprocess
import sys
from pathlib import Path

# A versão exata que apareceu no seu erro
TARGET_NDK_VERSION = "27.1.12297006"

def get_sdk_path():
    """Localiza o SDK do Android."""
    # Tenta ler do local.properties atual
    root_dir = Path.cwd()
    local_props = root_dir / "mobile" / "android" / "local.properties"
    
    if local_props.exists():
        with open(local_props, "r") as f:
            for line in f:
                if line.strip().startswith("sdk.dir"):
                    path_str = line.split("=")[1].strip()
                    path_str = path_str.replace("\\:", ":").replace("\\\\", "\\")
                    return Path(path_str)
    
    # Fallback
    return Path(os.environ["LOCALAPPDATA"]) / "Android" / "Sdk"

def find_sdkmanager(sdk_path):
    """Encontra o executável do sdkmanager."""
    print("🔍 Procurando sdkmanager...")
    for path in sdk_path.rglob("sdkmanager.bat"):
        return path
    return None

def install_ndk_27(sdk_path):
    """Instala a versão específica do NDK."""
    sdkmanager = find_sdkmanager(sdk_path)
    if not sdkmanager:
        print("❌ sdkmanager não encontrado.")
        return False

    package = f"ndk;{TARGET_NDK_VERSION}"
    print(f"⬇️  Instalando NDK {TARGET_NDK_VERSION}...")
    print("   (Isso pode demorar alguns minutos...)")
    
    cmd = f'echo y | "{str(sdkmanager)}" --install "{package}"'
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print("✅ NDK instalado com sucesso.")
        return True
    except subprocess.CalledProcessError:
        print("❌ Falha na instalação do NDK.")
        return False

def update_local_properties(sdk_path):
    """Atualiza o local.properties para apontar para o NDK 27."""
    ndk_path = sdk_path / "ndk" / TARGET_NDK_VERSION
    
    if not ndk_path.exists():
        print(f"❌ Erro: A pasta {ndk_path} não existe mesmo após instalação.")
        return False

    print(f"🔧 Atualizando local.properties para apontar para NDK 27...")
    
    props_file = Path.cwd() / "mobile" / "android" / "local.properties"
    
    # Formato seguro para Windows
    sdk_str = str(sdk_path).replace("\\", "\\\\").replace(":", "\\:")
    ndk_str = str(ndk_path).replace("\\", "\\\\").replace(":", "\\:")
    
    content = f"sdk.dir={sdk_str}\nndk.dir={ndk_str}\n"
    
    with open(props_file, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("✅ Configuração atualizada.")
    return True

def run_build():
    print("\n🚀 Tentando Build novamente...")
    # Chama o script de build existente que já configura o Java
    subprocess.run([sys.executable, "scripts/setup/fix_java_and_build.py"])

if __name__ == "__main__":
    sdk_path = get_sdk_path()
    if sdk_path.exists():
        if install_ndk_27(sdk_path):
            if update_local_properties(sdk_path):
                run_build()
    else:
        print(f"❌ SDK não encontrado em {sdk_path}")
