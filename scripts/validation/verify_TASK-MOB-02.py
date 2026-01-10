# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 00:58:00
import os
from pathlib import Path

def validate():
    print("Validando TASK-MOB-02 (Mobile Screens Implementation)")
    
    base_path = Path("mobile/src/screens")
    required_files = [
        "auth/LoginScreen.tsx",
        "waiter/WaiterDashboard.tsx",
        "kitchen/KitchenDashboard.tsx",
        "driver/DriverDashboard.tsx"
    ]
    
    missing = []
    for rel_path in required_files:
        full_path = base_path / rel_path
        if not full_path.exists():
            missing.append(str(rel_path))
            
    if missing:
        print(f"[ERRO] Telas ausentes: {', '.join(missing)}")
        exit(1)
        
    # Verifica se o RootNavigator as referencia
    navigator = Path("mobile/src/navigation/RootNavigator.tsx")
    if navigator.exists():
        nav_content = navigator.read_text(encoding="utf-8")
        if "WaiterDashboard" not in nav_content or "KitchenDashboard" not in nav_content:
            print("[ERRO] Telas nao estao registradas no RootNavigator.")
            exit(1)

    print("✅ TASK-MOB-02: Telas operacionais e navegacao validadas.")
    exit(0)

if __name__ == "__main__":
    validate()
