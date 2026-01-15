# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-15 12:20:00
import requests
import sys
import os
from datetime import datetime
from pathlib import Path

def run_healthcheck():
    print("🚀 Running INF-01: Infrastructure Healthcheck...")
    
    # Tenta localhost e 127.0.0.1 para robustez no Windows
    hosts = ["http://localhost:8000", "http://127.0.0.1:8000"]
    success = False
    details = ""
    
    for base_url in hosts:
        health_endpoint = f"{base_url}/health"
        try:
            print(f"   Trying {health_endpoint}...")
            response = requests.get(health_endpoint, timeout=2)
            if response.status_code == 200:
                data = response.json()
                db_status = data.get("services", {}).get("database", "down")
                if db_status != "up" and db_status != "healthy":
                    success = False
                    details = f"Database is {db_status}"
                else:
                    success = True
                    details = f"API and Database are ONLINE ({base_url})"
                    break # Sucesso, para de tentar
            else:
                details = f"HTTP Error: {response.status_code}"
        except Exception as e:
            details = f"Connection failed: {str(e)}"
            
    report_path = Path("governance/evidence/REPORT_INF_01.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# 📊 Healthcheck Report - INF-01\n\n")
        f.write(f"**Timestamp:** {datetime.now().isoformat()}\n")
        f.write(f"**Status:** {'✅ SUCCESS' if success else '❌ FAILURE'}\n")
        f.write(f"**Details:** {details}\n")
        
    if success:
        print(f"   ✅ {details}")
        return 0
    else:
        print(f"   ❌ {details}")
        return 1

if __name__ == "__main__":
    sys.exit(run_healthcheck())
