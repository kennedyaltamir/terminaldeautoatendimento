# DOMAIN: SRE
# LAST_MODIFIED: 2026-01-13 02:30:00
import requests
import sys
import os
from datetime import datetime
def probe_render():
    """
    INF-02: Render Health Probe.
    Valida o endpoint de produção real no Render.com.
    """
    url = os.getenv("RENDER_PROD_URL", "https://mesaflow-api.onrender.com/health")
    print(f"🚀 Probing Render Production: {url}")
    success = False
    details = ""
    try:
        start = datetime.now()
        res = requests.get(url, timeout=15)
        latency = (datetime.now() - start).total_seconds() * 1000
        if res.status_code == 200:
            success = True
            details = f"Status: 200 OK | Latency: {latency:.2f}ms"
        else:
            details = f"Status: {res.status_code} | Body: {res.text[:100]}"
    except Exception as e:
        details = f"Connection Failed: {str(e)}"
    report_path = "comunication/reports/REPORT_INF_02.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 🚀 Render Health Probe Report (INF-02)\n\n")
        f.write(f"- **Status:** {'✅ ONLINE' if success else '❌ OFFLINE'}\n")
        f.write(f"- **Details:** {details}\n")
        f.write(f"- **Timestamp:** {datetime.now().isoformat()}\n")
    return 0 if success else 1
if __name__ == "__main__":
    sys.exit(probe_render())
