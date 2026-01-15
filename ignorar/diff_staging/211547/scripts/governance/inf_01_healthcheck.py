# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 21:15:00
import requests
import sys
import io
from datetime import datetime

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def run_healthcheck():
    url = "http://localhost:8000/health"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            print("✅ API Online")
            return 0
        print(f"❌ API retornou {res.status_code}")
        return 1
    except Exception as e:
        print(f"❌ Falha de conexão: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_healthcheck())
