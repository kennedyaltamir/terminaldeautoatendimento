
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 10:30:00
import os
import sys
from pathlib import Path

class ProductionAuditor:
    def __init__(self):
        self.root = Path(".")
        self.errors = []

    def audit_security_docs(self):
        core_model = self.root / "app/models/core.py"
        if core_model.exists():
            content = core_model.read_text(encoding="utf-8")
            if "SECURITY POLICY" not in content or "THREAT MODEL" not in content:
                self.errors.append("DOCUMENTAÇÃO: Política de Segurança/Threat Model ausente no core.py")
            else:
                print("   ✅ Política de Segurança detectada no core.py")

    def audit_readme(self):
        readme = self.root / "README.md"
        required_terms = ["Command", "Event", "Consistency", "Idempotency", "Threat Model"]
        if readme.exists():
            content = readme.read_text(encoding="utf-8")
            for term in required_terms:
                if term not in content:
                    self.errors.append(f"README: Termo arquitetural obrigatório ausente: {term}")
            if not any(err.startswith("README") for err in self.errors):
                print("   ✅ README.md em conformidade com os padrões L6")

    def check_fmea(self):
        fmea_file = self.root / "docs/technical/FAILURE_MODES_ANALYSIS.md"
        if not fmea_file.exists():
            self.errors.append("FMEA: Documento de Failure Modes Analysis ausente.")
        else:
            print("   ✅ FMEA Document detectado.")

    def check_lock(self):
        if not (self.root / "docs/mobile/reports/PRODUCTION_LOCK_MOBILE.json").exists():
            self.errors.append("LOCK: PRODUCTION_LOCK_MOBILE.json não encontrado.")
        else:
            print("   ✅ PRODUCTION_LOCK_MOBILE detectado.")

    def run(self):
        print("🛡️  Iniciando Auditoria de Prontidão de Produção L6.3...")
        self.audit_security_docs()
        self.audit_readme()
        self.check_fmea()
        self.check_lock()

        if self.errors:
            print("\n❌ PRODUÇÃO BLOQUEADA POR INCONSISTÊNCIA ARQUITETURAL:")
            for err in self.errors: print(f"   - {err}")
            sys.exit(1)
        
        print("\n✨ SISTEMA HOMOLOGADO PARA PRODUÇÃO.")
        sys.exit(0)

if __name__ == "__main__":
    ProductionAuditor().run()

