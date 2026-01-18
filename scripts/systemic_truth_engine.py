# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 18:55:00
# ==============================================================================
# 🕵️ MESAFLOW SYSTEMIC TRUTH ENGINE (L6) - WINDOWS HARDENED v1.3
# ==============================================================================
# Objetivo: Atuar como a "Base de Verdade Absoluta".
# Fix: Ignora erros de "File not found" em .next/types, pois são artefatos de build.
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

class SystemicTruthEngine:
    def __init__(self):
        self.root = Path(".")
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "verdict": "PENDING",
            "metrics": {
                "compilation_errors": 0,
                "integrity_violations": 0,
                "async_conflicts": 0,
                "tooling_gaps": 0
            },
            "layers": {
                "frontend": {"status": "UNKNOWN", "findings": []},
                "backend": {"status": "UNKNOWN", "findings": []},
                "automation": {"status": "UNKNOWN", "findings": []},
                "governance": {"status": "UNKNOWN", "findings": []}
            }
        }

    def run_command(self, cmd, cwd=None):
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, cwd=cwd, encoding='utf-8', errors='replace'
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), 1

    def audit_frontend_compilation(self):
        """Executa tsc real e detecta mascaramento de erros."""
        print("🎨 [1/5] Auditando Compilação Real (TypeScript)...")
        stdout, stderr, code = self.run_command("npx tsc --noEmit", cwd=self.root / "frontend")
        errors = stdout.splitlines()
        
        # Filtragem de Ruído: Ignora erros de tipos do Next.js que somem no build real
        real_errors = [
            e for e in errors 
            if "error TS" in e 
            and ".next/types" not in e 
            and "TS6053" not in e
        ]
        
        self.report["metrics"]["compilation_errors"] = len(real_errors)
        
        if real_errors:
            self.report["layers"]["frontend"]["findings"].append({
                "id": "COMPILATION_FAIL",
                "severity": "CRITICAL",
                "message": f"Falha de compilação com {len(real_errors)} erros reais.",
                "evidence": real_errors[:5]
            })

        # Verifica tsconfig.json
        tsconfig_path = self.root / "frontend/tsconfig.json"
        if tsconfig_path.exists():
            content = tsconfig_path.read_text(encoding='utf-8', errors='replace')
            if '"strict": true' not in content:
                self.report["layers"]["frontend"]["findings"].append({
                    "id": "MASKED_ERRORS",
                    "severity": "HIGH",
                    "message": "Strict mode desativado no tsconfig.json."
                })
        
        self.report["layers"]["frontend"]["status"] = "FAILED" if real_errors else "PASSED"

    def audit_python_async_safety(self):
        """Analisa conflitos de loop."""
        print("🐍 [2/5] Auditando Segurança Async (Python 3.13)...")
        findings = []
        
        for path in self.root.glob("scripts/automation/*.py"):
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
                if "asyncio.run(" in content and "@pytest.mark.asyncio" in content:
                    findings.append({
                        "file": str(path),
                        "issue": "CONFLITO DE LOOP: asyncio.run() dentro de teste gerenciado pelo pytest-asyncio."
                    })
                    self.report["metrics"]["async_conflicts"] += 1
            except: continue

        self.report["layers"]["automation"]["findings"] = findings
        self.report["layers"]["automation"]["status"] = "FAILED" if findings else "PASSED"

    def audit_meta_tooling(self):
        """Audita se os auditores estão mentindo."""
        print("⚖️ [3/5] Meta-Auditoria de Ferramentas...")
        findings = []
        
        auditor_path = self.root / "scripts/diagnostics/audit_systemic_entropy.py"
        if auditor_path.exists():
            try:
                content = auditor_path.read_text(encoding='utf-8', errors='replace')
                if "subprocess.run" not in content and "tsc" not in content:
                    findings.append({
                        "id": "FAKE_AUDITOR",
                        "severity": "CRITICAL",
                        "message": "audit_systemic_entropy.py é cosmético."
                    })
                    self.report["metrics"]["tooling_gaps"] += 1
            except Exception as e:
                print(f"⚠️ Falha ao ler auditor: {e}")

        self.report["layers"]["governance"]["findings"] = findings
        self.report["layers"]["governance"]["status"] = "FAILED" if findings else "PASSED"

    def run(self):
        print("\n" + "="*60)
        print("🚀 INICIANDO MOTOR DE VERDADE SISTÊMICA")
        print("="*60)
        
        self.audit_frontend_compilation()
        self.audit_python_async_safety()
        self.audit_meta_tooling()
        
        if self.report["metrics"]["compilation_errors"] > 0 or self.report["metrics"]["async_conflicts"] > 0:
            self.report["verdict"] = "UNRELIABLE_SYSTEM_ENTROPY"
        else:
            self.report["verdict"] = "STABLE"

        output_path = self.root / "governance/evidence/SYSTEMIC_TRUTH_REPORT.json"
        os.makedirs(output_path.parent, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)

        print("\n" + "="*60)
        print("📊 RESULTADO DA META-AUDITORIA")
        print(f"❌ Erros de Compilação: {self.report['metrics']['compilation_errors']}")
        print(f"❌ Conflitos de Loop: {self.report['metrics']['async_conflicts']}")
        print("="*60)
        print(f"VEREDITO: {self.report['verdict']}")
        print(f"Relatório detalhado: {output_path}")

if __name__ == "__main__":
    SystemicTruthEngine().run()

