
# DOMAIN: DEVOPS_SCRIPTS
import os
import sys
from pathlib import Path

def verify():
    screens_dir = Path("mobile/src/screens")
    required_import = "ErrorStateView"
    critical_screens = ["OrdersScreen", "WaiterTablesScreen", "DriverDashboard", "KitchenDashboard"]
    
    missing = []
    for screen in critical_screens:
        file_path = screens_dir / f"{screen}.tsx"
        if file_path.exists():
            if required_import not in file_path.read_text():
                missing.append(screen)
        else:
            # Tenta procurar em subpastas
            found = list(screens_dir.rglob(f"{screen}.tsx"))
            if not found or required_import not in found[0].read_text():
                missing.append(screen)

    if missing:
        print(f"🚨 BLOQUEIO: Telas críticas sem tratamento de erro visual: {missing}")
        sys.exit(1)
    
    print("✅ Resiliência visual validada nas telas críticas.")
    sys.exit(0)

if __name__ == "__main__":
    verify()

