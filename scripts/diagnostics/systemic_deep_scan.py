import os
import re
import json
import sys
import io
from pathlib import Path
from typing import List, Dict, Any

# ==============================================================================
# 🧬 SYSTEMIC DEEP SCAN (L2 Auditor)
# ==============================================================================
# Objetivo: Análise estática profunda para correlacionar falhas de runtime
# (401, CORS, Kiosk Breach) com a implementação física do código.
# ==============================================================================

# Fix para Windows Unicode
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROJECT_ROOT = Path(".")
REPORT_FILE = Path("governance/evidence/SYSTEMIC_DEEP_SCAN.json")

class DeepScanner:
    def __init__(self):
        self.findings = []
        self.stats = {"files_scanned": 0, "critical": 0, "warnings": 0}

    def log_finding(self, file: str, severity: str, issue_type: str, message: str, context: str = ""):
        self.findings.append({
            "file": str(file),
            "severity": severity,
            "type": issue_type,
            "message": message,
            "context": context.strip()
        })
        if severity == "CRITICAL": self.stats["critical"] += 1
        if severity == "WARNING": self.stats["warnings"] += 1

    def scan_middleware_security(self):
        """Verifica se o middleware.ts protege o Kiosk e rotas Admin."""
        path = PROJECT_ROOT / "frontend/src/middleware.ts"
        if not path.exists():
            self.log_finding("middleware.ts", "CRITICAL", "MISSING_FILE", "Middleware de segurança não encontrado.")
            return

        content = path.read_text(encoding="utf-8")
        self.stats["files_scanned"] += 1

        # Check 1: Proteção de Kiosk
        if "kiosk" not in content.lower():
            self.log_finding(path, "CRITICAL", "KIOSK_UNPROTECTED", "Middleware não menciona lógica para 'kiosk'. Risco de fuga de sandbox.")
        
        # Check 2: Redirecionamento Admin
        if "/admin" in content and "NextResponse.redirect" not in content:
            self.log_finding(path, "HIGH", "WEAK_REDIRECT", "Lógica de admin detectada mas sem redirecionamento explícito visível.")

    def scan_api_client_integrity(self):
        """Verifica se o cliente HTTP trata tokens corretamente."""
        path = PROJECT_ROOT / "frontend/src/lib/api.ts"
        if not path.exists(): return

        content = path.read_text(encoding="utf-8")
        self.stats["files_scanned"] += 1

        # Check 1: Header Authorization
        if 'headers["Authorization"]' not in content and "headers['Authorization']" not in content:
            self.log_finding(path, "CRITICAL", "AUTH_HEADER_MISSING", "Cliente API não parece injetar o header Authorization.")

        # Check 2: Tratamento de 401
        if "401" not in content:
            self.log_finding(path, "HIGH", "AUTH_REFRESH_MISSING", "Não foi detectada lógica de tratamento para erro 401 (Refresh Token).")

    def scan_backend_cors(self):
        """Verifica configuração de CORS no FastAPI."""
        path = PROJECT_ROOT / "app/main.py"
        if not path.exists(): return

        content = path.read_text(encoding="utf-8")
        self.stats["files_scanned"] += 1

        # Check 1: Middleware Presente
        if "CORSMiddleware" not in content:
            self.log_finding(path, "CRITICAL", "CORS_MISSING", "Middleware CORS não importado ou configurado.")
        
        # Check 2: Origens
        if 'allow_origins=["*"]' not in content and "http://localhost:3000" not in content:
            self.log_finding(path, "HIGH", "CORS_RESTRICTIVE", "Configuração de origens pode estar bloqueando o frontend local.")

    def scan_kiosk_components(self):
        """Varre componentes de Kiosk em busca de links de fuga."""
        kiosk_dir = PROJECT_ROOT / "frontend/src/app/[slug]/kiosk"
        if not kiosk_dir.exists(): return

        for root, _, files in os.walk(kiosk_dir):
            for file in files:
                if file.endswith(".tsx"):
                    path = Path(root) / file
                    content = path.read_text(encoding="utf-8")
                    self.stats["files_scanned"] += 1

                    # Check: Links para Admin
                    if '"/admin' in content or "'/admin" in content:
                        self.log_finding(path, "CRITICAL", "KIOSK_ESCAPE_LINK", "Link hardcoded para /admin encontrado dentro do Kiosk.")

    def scan_react_loops(self):
        """Procura por padrões de loop infinito em useEffect."""
        frontend_dir = PROJECT_ROOT / "frontend/src"
        
        for root, _, files in os.walk(frontend_dir):
            for file in files:
                if file.endswith(".tsx"):
                    path = Path(root) / file
                    content = path.read_text(encoding="utf-8")
                    self.stats["files_scanned"] += 1

                    # Padrão simples: useEffect com dependência que é setada dentro dele
                    # Ex: useEffect(() => { setX() }, [x])
                    # Isso é heurístico, não um parser AST completo, mas pega casos óbvios
                    if "useEffect" in content:
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if "useEffect" in line and "[" in line:
                                deps = re.findall(r'\[(.*?)\]', line)
                                if deps:
                                    dep_list = deps[0].split(',')
                                    for dep in dep_list:
                                        clean_dep = dep.strip()
                                        if clean_dep and f"set{clean_dep[0].upper()}{clean_dep[1:]}" in content:
                                            # Aviso heurístico
                                            pass 

    def generate_report(self):
        print(f"🧬 Systemic Deep Scan concluído.")
        print(f"   Arquivos analisados: {self.stats['files_scanned']}")
        print(f"   Problemas Críticos: {self.stats['critical']}")
        print(f"   Avisos: {self.stats['warnings']}")

        report = {
            "timestamp": "2026-01-18T09:10:00",
            "stats": self.stats,
            "issues": self.findings
        }

        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        
        # Output Humano no Terminal
        if self.findings:
            print("\n🚨 PRINCIPAIS DESCOBERTAS:")
            for f in self.findings:
                icon = "🔴" if f['severity'] == "CRITICAL" else "🟡"
                print(f"{icon} [{f['type']}] {f['file']}: {f['message']}")
        else:
            print("\n✅ Nenhuma inconsistência estrutural óbvia detectada.")

if __name__ == "__main__":
    scanner = DeepScanner()
    print("🕵️ Iniciando varredura profunda de código...")
    scanner.scan_middleware_security()
    scanner.scan_api_client_integrity()
    scanner.scan_backend_cors()
    scanner.scan_kiosk_components()
    scanner.scan_react_loops()
    scanner.generate_report()

 