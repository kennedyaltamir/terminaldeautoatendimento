import os
import subprocess
import sys
from pathlib import Path

def build_android():
    # Define caminhos
    root_dir = Path.cwd()
    android_dir = root_dir / "mobile" / "android"

    # Validações
    if not android_dir.exists():
        print("❌ Pasta 'mobile/android' não encontrada.")
        print("   Execute: python scripts/setup/fix_mobile_build.py")
        return

    if "JAVA_HOME" not in os.environ:
        print("⚠️  AVISO: JAVA_HOME não está definido nas variáveis de ambiente.")
        print("   O Gradle precisa do Java (JDK 17) para rodar.")

    # Define o comando do Gradle baseado no SO
    gradlew = "gradlew.bat" if os.name == "nt" else "./gradlew"
    gradle_path = android_dir / gradlew

    if not gradle_path.exists():
        print(f"❌ Arquivo {gradlew} não encontrado em {android_dir}")
        return

    print(f"🚀 Iniciando Build Nativo Android (Release)...")
    print(f"📂 Diretório: {android_dir}")
    print("⏳ Aguarde... Compilando APK...")

    try:
        # Executa o Gradle Wrapper capturando a saída
        # Usamos shell=True no Windows
        process = subprocess.run(
            [str(gradle_path), "assembleRelease"], 
            cwd=android_dir, 
            check=True, 
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        print("\n✅ Build Concluído com Sucesso!")
        
        # Caminho do APK gerado
        apk_path = android_dir / "app" / "build" / "outputs" / "apk" / "release" / "app-release.apk"
        
        if apk_path.exists():
            print(f"📦 APK Localizado: {apk_path}")
            if os.name == "nt":
                os.startfile(apk_path.parent)
        else:
            print("⚠️ O comando terminou, mas não encontrei o arquivo 'app-release.apk'.")

    except subprocess.CalledProcessError as e:
        print("\n❌ FALHA NO BUILD.")
        print("--- LOG DE ERRO (Últimas 50 linhas) ---")
        # Imprime as últimas 50 linhas do stderr para diagnóstico
        lines = e.stderr.splitlines()
        for line in lines[-50:]:
            print(line)
        print("---------------------------------------")
        print("👉 Dica: Se o erro for sobre NDK/CMake, rode: python scripts/setup/install_android_platform.py")
        
    except KeyboardInterrupt:
        print("\n🛑 Build cancelado pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    build_android()
