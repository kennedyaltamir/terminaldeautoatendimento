# DOMAIN: SRE
# LAST_MODIFIED: 2026-01-13 02:30:00
import requests
import sys
import time
from datetime import datetime
def check_latency():
    """
    INF-03: Vercel to Backend Latency Check.
    Simula a latência percebida pelo frontend.
    """
    backend_url = "https://mesaflow-api.onrender.com/api/health"
    print(f"📡 Checking Latency: {backend_url}")
    samples = []
    for i in range(3):
        try:
            start = time.time()
            requests.get(backend_url, timeout=10)
            samples.append((time.time() - start) * 1000)
        except:
            samples.append(None)
    valid_samples = [s for s in samples if s is not None]
    avg_latency = sum(valid_samples) / len(valid_samples) if valid_samples else 0
    success = avg_latency > 0 and avg_latency < 500
    report_path = "comunication/reports/REPORT_INF_03.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 📡 Vercel Latency Check (INF-03)\n\n")
        f.write(f"- **Average Latency:** {avg_latency:.2f}ms\n")
        f.write(f"- **Threshold:** 500ms\n")
        f.write(f"- **Verdict:** {'✅ PASS' if success else '❌ FAIL'}\n")
    return 0 if success else 1
if __name__ == "__main__":
    sys.exit(check_latency())