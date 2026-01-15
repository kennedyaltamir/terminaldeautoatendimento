
import os
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("testesvisuais")
OUTPUT_FILE = "relatorio_consolidado_optimus.txt"

def consolidate():
    latest = sorted([d for d in BASE_DIR.iterdir() if d.is_dir() and d.name.startswith("run_")])[-1]
    print(f"🔄 Consolidando: {latest.name}")
    
    buffer = [f"RELATÓRIO CONSOLIDADO: {latest.name}\n" + "="*40]
    
    for page_dir in sorted(latest.iterdir()):
        if not page_dir.is_dir(): continue
        report = page_dir / "docs" / "relatorio_forense_v9.md"
        if report.exists():
            buffer.append(f"\n--- [PÁGINA] {page_dir.name} ---\n")
            buffer.append(report.read_text(encoding="utf-8"))
            
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(buffer))
    print(f"✅ Gerado: {OUTPUT_FILE}")

if __name__ == "__main__":
    consolidate()

