# DOMAIN: MOBILE
# LAST_MODIFIED: 2026-01-13 02:30:00
import subprocess
import sys
import os
import json
def probe_expo():
    """
    INF-04: Expo Runtime Probe.
    Verifica se o ambiente local está pronto para rodar o Expo Go.
    """
    print("📱 Probing Expo Runtime...")
    results = {}
    # 1. Check Node
    try:
        node_v = subprocess.check_output(["node", "-v"]).decode().strip()
        results["node"] = {"status": "OK", "version": node_v}
    except:
        results["node"] = {"status": "FAIL"}
    # 2. Check Expo CLI
    try:
        expo_v = subprocess.check_output(["npx", "expo", "-v"], shell=True).decode().strip()
        results["expo"] = {"status": "OK", "version": expo_v}
    except:
        results["expo"] = {"status": "FAIL"}
    # 3. Check mobile/package.json
    pkg_path = "mobile/package.json"
    if os.path.exists(pkg_path):
        with open(pkg_path, 'r') as f:
            pkg = json.load(f)
            results["sdk"] = pkg.get("dependencies", {}).get("expo", "unknown")
    success = results.get("node", {}).get("status") == "OK"
    report_path = "comunication/reports/REPORT_INF_04.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 📱 Expo Runtime Probe (INF-04)\n\n")
        f.write(json.dumps(results, indent=2))
    return 0 if success else 1
if __name__ == "__main__":
    sys.exit(probe_expo())
