import sys
import os

def verify():
    print("🔍 Verificando TASK-MOB-01: Otimização do Global Clock...")

    target_file = "mobile/src/services/global.clock.service.ts"

    if not os.path.exists(target_file):
        print(f"❌ Arquivo {target_file} não encontrado.")
        sys.exit(1)

    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Verifica importação do AppState
    if "import { AppState" not in content:
        print("❌ AppState não importado.")
        sys.exit(1)

    # 2. Verifica listener de mudança de estado
    if "AppState.addEventListener" not in content:
        print("❌ Listener de AppState não configurado.")
        sys.exit(1)

    # 3. Verifica lógica de pausa/retomada
    if "stopTimer()" not in content or "startTimer()" not in content:
        print("❌ Métodos de controle do timer ausentes.")
        sys.exit(1)

    # 4. Verifica se o intervalo é limpo no background
    if "clearInterval" not in content:
        print("❌ clearInterval não encontrado (Memory Leak potencial).")
        sys.exit(1)

    print("✅ TASK-MOB-01: Lógica de economia de energia implementada corretamente.")
    sys.exit(0)

if __name__ == "__main__":
    verify()
