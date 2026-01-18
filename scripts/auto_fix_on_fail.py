
import subprocess
import time

def recover():
    print("   🔧 L6 Auto-Fix: Tentando recuperação de estado...")
    # 1. Tenta fechar teclado
    subprocess.run("adb shell input keyevent 4", shell=True)
    time.sleep(0.5)
    # 2. Tenta scroll para encontrar elemento escondido
    subprocess.run("adb shell input swipe 500 1500 500 500 300", shell=True)
    time.sleep(1)

def retry_action(step_fn, retries=2):
    """
    Wrapper para tentar uma ação, executar auto-fix se falhar, e tentar novamente.
    """
    for i in range(retries + 1):
        try:
            return step_fn()
        except Exception as e:
            if i < retries:
                print(f"   ⚠️  Falha na tentativa {i+1}. Iniciando Auto-Fix...")
                recover()
            else:
                print("   ❌ Todas as tentativas de Auto-Fix falharam.")
                raise e

