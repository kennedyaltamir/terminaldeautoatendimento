# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 00:55:00
import os
import subprocess
import json
import sys
from pathlib import Path

def check_command(cmd):
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, shell=True)
        return True
    except:
        return False

def run_doctor():
    print("MesaFlow Mobile Doctor - Iniciando Diagnostico")
    
    mobile_dir = Path("mobile")
    results = []
    all_ok = True

    # 1. Verifica existência da pasta
    if not mobile_dir.exists():
        print("[ERRO] Pasta 'mobile/' nao encontrada.")
        sys.exit(1)

    # 2. Verifica Node.js
    node_ok = check_command("node -v")
    results.append(("Node.js Instalado", node_ok))
    if not node_ok: all_ok = False

    # 3. Verifica package.json
    pkg_path = mobile_dir / "package.json"
    pkg_ok = pkg_path.exists()
    results.append(("package.json existe", pkg_ok))
    
    if pkg_ok:
        try:
            with open(pkg_path, 'r') as f:
                pkg = json.load(f)
                expo_ver = pkg.get("dependencies", {}).get("expo", "N/A")
                results.append((f"Expo SDK ({expo_ver})", True))
        except Exception:
            results.append(("package.json (Erro de Leitura)", False))
            all_ok = False
    else:
        all_ok = False

    # 4. Verifica node_modules
    nm_ok = (mobile_dir / "node_modules").exists()
    results.append(("node_modules instalado", nm_ok))
    if not nm_ok: all_ok = False

    # 5. Verifica Assets Críticos
    assets_dir = mobile_dir / "assets"
    assets_exist = assets_dir.exists()
    results.append(("Pasta assets/", assets_exist))
    
    if assets_exist:
        icon_ok = (assets_dir / "icon.png").exists()
        results.append(("Icone (assets/icon.png)", icon_ok))
        if not icon_ok: all_ok = False
    else:
        all_ok = False

    print(f"\n{'CHECK':<30} | {'STATUS':<10}")
    print("-" * 45)
    for check, status in results:
        print(f"{check:<30} | {'[OK]' if status else '[FALHA]'}")

    if not all_ok:
        print("\n[AVISO] O diagnostico encontrou problemas que impedem o boot.")
        sys.exit(1)
    
    print("\nAmbiente mobile saudavel.")
    sys.exit(0)

if __name__ == "__main__":
    run_doctor()
