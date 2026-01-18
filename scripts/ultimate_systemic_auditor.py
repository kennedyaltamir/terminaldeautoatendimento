# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 18:50:00
# ==============================================================================
# 🕵️ MESAFLOW ULTIMATE SYSTEMIC AUDITOR (L6) - ASYNC HARDENED
# ==============================================================================
import os
import sys
import json
import subprocess
import io
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class UltimateAuditor:
    def __init__(self):
        self.root = Path(".")
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "verdict": "PENDING",
            "confidence_score": 100,
            "metrics": {
                "compilation_errors": 0,
                "file_corruptions": 0,
                "async_loop_conflicts": 0
            },
            "findings": []
        }

    def run_tsc(self):
        print("🎨 [1/3] Auditando Compilação TypeScript...")
        res = subprocess.run(
            "npx tsc --noEmit", 
            cwd=self.root / "frontend", shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace'
        )
        errors = res.stdout.splitlines()
        self.report["metrics"]["compilation_errors"] = len(errors)
        
        duplicates = [e for e in errors if "TS2300" in e]
        self.report["metrics"]["file_corruptions"] = len(duplicates)
        
        if duplicates:
            self.report["confidence_score"] -= 50

    def audit_async_usage(self):
        print("🐍 [2/3] Auditando Padrões Async...")
        # Verifica se há asyncio.run em arquivos que não deveriam ter
        for path in self.root.glob("scripts/**/*.py"):
            if path.name == "ultimate_systemic_auditor.py": continue
            content = path.read_text(encoding='utf-8', errors='replace')
            
            if "asyncio.run(" in content and "@pytest.mark.asyncio" in content:
                self.report["metrics"]["async_loop_conflicts"] += 1
                self.report["confidence_score"] -= 10

    def run(self):
        self.run_tsc()
        self.audit_async_usage()
        
        self.report["verdict"] = "STABLE" if self.report["confidence_score"] > 90 else "UNRELIABLE"
        
        output_path = self.root / "governance/evidence/ULTIMATE_TRUTH_REPORT.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
            
        print(f"\n📊 RESULTADO: {self.report['verdict']} (Score: {self.report['confidence_score']})")

if __name__ == "__main__":
    # ASYNC_SAFE: Este script é síncrono para evitar conflitos de loop durante a auditoria
    UltimateAuditor().run()

