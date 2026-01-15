import os
import shutil
import sys
import subprocess
import time
from pathlib import Path

def log(msg):
    print(f"   {msg}")

def kill_zombies():
    print("💀 Matando processos zumbis (Java/Node/ADB)...")
    if os.name == 'nt': # Windows
        subprocess.run("taskkill /F /IM java.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("taskkill /F /IM node.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("taskkill /F /IM adb.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("taskkill /F /IM openjdk.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        os.system("pkill -f java")
        os.system("pkill -f node")
    
    time.sleep(2) # Dá tempo para o SO liberar os arquivos

def rmtree_error_handler(func, path, exc_info):
    """Força a deleção de arquivos travados no Windows."""
    import stat
    try:
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
        func(path)
    except Exception as e:
        print(f"⚠️  Não foi possível deletar: {path} ({e})")

def deep_clean():
    print("☢️  Iniciando Limpeza Nuclear do Ambiente Mobile...")
    
    # 1. Matar processos que seguram arquivos
    kill_zombies()
    
    root_dir = Path.cwd()
    mobile_dir = root_dir / "mobile"
    android_dir = mobile_dir / "android"
    node_modules = mobile_dir / "node_modules"
    
    # 2. Limpar pastas de build e dependências
    targets = [
        android_dir,                    # Pasta nativa inteira
        node_modules,                   # Dependências JS (provavelmente corrompidas)
        mobile_dir / ".expo",           # Cache do Expo
        mobile_dir / "package-lock.json" # Lockfile (opcional, mas bom para reset)
    ]

    for target in targets:
        if target.exists():
            log(f"🗑️  Deletando: {target.name}...")
            try:
                if target.is_dir():
                    shutil.rmtree(target, onerror=rmtree_error_handler)
                else:
                    os.remove(target)
            except Exception as e:
                log(f"❌ Erro ao deletar {target.name}: {e}")

    # 3. Reinstalar Dependências
    print("\n📦 Reinstalando dependências (npm install)...")
    # --legacy-peer-deps é crucial para React Native hoje em dia
    try:
        subprocess.run("npm install --legacy-peer-deps", cwd=mobile_dir, shell=True, check=True)
    except subprocess.CalledProcessError:
        print("❌ Falha no npm install. Verifique sua conexão ou permissões.")
        return

    # 4. Gerar Projeto Nativo (Prebuild)
    print("\n🔄 Regenerando projeto nativo (Prebuild)...")
    try:
        # npx expo prebuild gera a pasta android/ baseada no app.json
        cmd = "npx expo prebuild --platform android --clean"
        if os.name == 'nt':
            cmd = f"cmd /c {cmd}"
            
        subprocess.run(cmd, cwd=mobile_dir, shell=True, check=True)
        print("\n✅ Prebuild concluído com sucesso!")
        print("🚀 Agora você pode rodar: python scripts/setup/build_android.py")
        
    except subprocess.CalledProcessError:
        print("\n❌ Falha no Prebuild. Verifique se o 'app.json' está correto.")

if __name__ == "__main__":
    deep_clean()
