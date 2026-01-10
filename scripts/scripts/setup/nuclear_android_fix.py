import os
import subprocess
import re
import sys
from pathlib import Path

def run_cmd(cmd, cwd=None, env=None):
    try:
        subprocess.run(cmd, shell=True, check=True, cwd=cwd, env=env)
        return True
    except:
        return False

def main():
    print("☢️  Iniciando Reparo Nuclear do Ambiente Android...")

    # 1. Definir caminhos reais
    real_sdk_path = r"C:\Users\Kennedy Oliveira\AppData\Local\Android\Sdk"
    root_dir = Path.cwd()
    android_dir = root_dir / "mobile" / "android"
    
    if not os.path.exists(real_sdk_path):
        print(f"❌ SDK não encontrado em {real_sdk_path}")
        return

    # 2. Criar Unidade Virtual S: para remover espaços do caminho
    print("🔗 Mapeando SDK para unidade virtual S: (para remover espaços)...")
    os.system("subst S: /d >nul 2>&1") # Remove se já existir
    if not run_cmd(f'subst S: "{real_sdk_path}"'):
        print("❌ Falha ao criar unidade S:. Tente rodar o terminal como Administrador.")
        return
    
    print("✅ Unidade S: mapeada com sucesso.")

    # 3. Atualizar local.properties (SEM ndk.dir, apenas sdk.dir virtual)
    print("🔧 Atualizando local.properties...")
    props_file = android_dir / "local.properties"
    with open(props_file, "w", encoding="utf-8") as f:
        f.write("sdk.dir=S:/\n")
    
    # 4. Forçar NDK 26 no build.gradle (Root e App)
    print("🔧 Forçando NDK 26.1.10909125 nos arquivos Gradle...")
    ndk_v = "26.1.10909125"
    
    files_to_patch = [
        android_dir / "build.gradle",
        android_dir / "app" / "build.gradle"
    ]

    for fpath in files_to_patch:
        if fpath.exists():
            content = fpath.read_text(encoding="utf-8")
            # Atualiza ndkVersion se existir, ou insere
            if "ndkVersion" in content:
                content = re.sub(r'ndkVersion\s*=?\s*["\'].*["\']', f'ndkVersion = "{ndk_v}"', content)
            else:
                content = re.sub(r'android\s*\{', f'android {{\n    ndkVersion = "{ndk_v}"', content)
            fpath.write_text(content, encoding="utf-8")

    # 5. Configurar Java 17
    java_home = r"C:\Program Files\Microsoft\jdk-17.0.17.10-hotspot"
    env = os.environ.copy()
    env["JAVA_HOME"] = java_home
    env["PATH"] = f"{java_home}\\bin;" + env["PATH"]

    # 6. Limpeza Agressiva e Build
    print("\n🧹 Limpando cache do Gradle (Clean)...")
    gradlew = str(android_dir / "gradlew.bat")
    
    run_cmd(f'"{gradlew}" clean', cwd=android_dir, env=env)

    print("\n🚀 Iniciando Compilação Final do APK...")
    if run_cmd(f'"{gradlew}" assembleRelease', cwd=android_dir, env=env):
        apk_path = android_dir / "app" / "build" / "outputs" / "apk" / "release" / "app-release.apk"
        print(f"\n🏆 SUCESSO! APK gerado sem erros de path: {apk_path}")
        os.startfile(apk_path.parent)
    else:
        print("\n❌ Build falhou. Se o erro persistir, reinicie o computador para liberar a unidade S:.")

if __name__ == "__main__":
    main()
