import os
import sys
import re
import json
import ast
from pathlib import Path
from typing import List, Dict, Any

# ==============================================================================
# 🕵️ REACT LOOP DETECTOR & ARCHITECTURE VALIDATOR (L7)
# ==============================================================================
# Objetivo: Analisar estaticamente código React/Next.js para detectar:
# 1. Loops de renderização (useEffect + setState + deps instáveis)
# 2. Conflitos de autoridade de estado (Polling vs Local State)
# 3. Fragilidade em testes E2E (Reloads, Timeouts, Seletores fracos)
# ==============================================================================

TARGET_DIRS = ["frontend/src/app", "frontend/src/components", "frontend/tests"]
REPORT_FILE = "governance/evidence/REACT_ARCHITECTURE_REPORT.md"
JSON_REPORT_FILE = "governance/evidence/react_architecture_report.json"

class ReactAnalyzer:
    def __init__(self):
        self.issues = []
        self.stats = {"files_scanned": 0, "critical": 0, "warnings": 0}

    def scan_project(self):
        print("🔍 Iniciando varredura profunda de arquitetura React...")
        for target_dir in TARGET_DIRS:
            path = Path(target_dir)
            if not path.exists(): continue
            
            for file_path in path.rglob("*"):
                if file_path.suffix in [".tsx", ".ts"]:
                    self.analyze_file(file_path)
        
        self.generate_reports()
        return self.stats["critical"]

    def analyze_file(self, file_path: Path):
        self.stats["files_scanned"] += 1
        try:
            content = file_path.read_text(encoding="utf-8")
            
            # 1. Análise de Loops de Renderização (Heurística Avançada)
            self.detect_render_loops(file_path, content)
            
            # 2. Análise de Conflito de Estado
            self.detect_state_conflicts(file_path, content)
            
            # 3. Análise de Testes E2E (Se for arquivo de teste)
            if "tests" in str(file_path):
                self.detect_test_fragility(file_path, content)
                
        except Exception as e:
            print(f"⚠️ Erro ao analisar {file_path}: {e}")

    def detect_render_loops(self, file_path: Path, content: str):
        # Padrão: useEffect chamando setState de uma variável que está nas dependências
        # Ex: useEffect(() => { setOrders(...) }, [orders])
        
        # Regex simplificado para capturar useEffect
        effects = re.finditer(r"useEffect\(\(\)\s*=>\s*{(.*?)},\s*\[(.*?)\]\)", content, re.DOTALL)
        
        for match in effects:
            body = match.group(1)
            deps = match.group(2)
            
            # Extrai setters chamados no corpo
            setters = re.findall(r"set(\w+)\(", body)
            
            # Verifica se a variável correspondente está nas dependências
            for setter in setters:
                var_name = setter[0].lower() + setter[1:] # setOrders -> orders
                
                # Verifica dependência direta
                if var_name in deps:
                    # Exceção: Se houver um if de guarda, pode ser seguro (heurística simples)
                    if f"if (!{var_name})" not in body and f"if ({var_name} !==" not in body:
                        self.add_issue(
                            file_path, 
                            "CRITICAL", 
                            "REACT_EFFECT_LOOP", 
                            f"Loop potencial: 'set{setter}' chamado em useEffect que depende de '{var_name}'."
                        )

    def detect_state_conflicts(self, file_path: Path, content: str):
        # Padrão: Polling (setInterval) e WebSocket atualizando o mesmo estado
        has_polling = "setInterval" in content
        has_websocket = "useWebSocket" in content
        has_set_state = "setState" in content or "setOrders" in content # Exemplo
        
        if has_polling and has_websocket and has_set_state:
            self.add_issue(
                file_path,
                "WARNING",
                "STATE_AUTHORITY_CONFLICT",
                "Polling e WebSocket detectados no mesmo componente. Risco de Race Condition na atualização de estado."
            )

    def detect_test_fragility(self, file_path: Path, content: str):
        # 1. Reload
        if "page.reload" in content:
            self.add_issue(
                file_path,
                "WARNING",
                "FLAKY_TEST_PATTERN",
                "Uso de 'page.reload()' detectado. Isso limpa o estado da aplicação e pode causar falhas em testes de SPA."
            )
            
        # 2. Hard Wait
        if "waitForTimeout" in content:
            self.add_issue(
                file_path,
                "WARNING",
                "FLAKY_TEST_PATTERN",
                "Uso de 'waitForTimeout' detectado. Prefira 'waitForSelector' ou asserções com retry."
            )

    def add_issue(self, file: Path, severity: str, type_: str, message: str):
        issue = {
            "file": str(file),
            "severity": severity,
            "type": type_,
            "message": message
        }
        self.issues.append(issue)
        if severity == "CRITICAL": self.stats["critical"] += 1
        if severity == "WARNING": self.stats["warnings"] += 1
        
        icon = "🔴" if severity == "CRITICAL" else "🟡"
        print(f"   {icon} [{type_}] {file.name}: {message}")

    def generate_reports(self):
        # JSON Report
        os.makedirs(Path(JSON_REPORT_FILE).parent, exist_ok=True)
        with open(JSON_REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump({"stats": self.stats, "issues": self.issues}, f, indent=2)
            
        # Markdown Report
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write("# 🕵️ React Architecture Audit Report\n\n")
            f.write(f"**Files Scanned:** {self.stats['files_scanned']}\n")
            f.write(f"**Critical Issues:** {self.stats['critical']}\n")
            f.write(f"**Warnings:** {self.stats['warnings']}\n\n")
            
            if self.issues:
                f.write("## 🚨 Detected Issues\n\n")
                for issue in self.issues:
                    icon = "🔴" if issue['severity'] == "CRITICAL" else "🟡"
                    f.write(f"### {icon} {issue['type']}\n")
                    f.write(f"- **File:** `{issue['file']}`\n")
                    f.write(f"- **Details:** {issue['message']}\n\n")
            else:
                f.write("✅ No architectural issues detected.\n")
                
        print(f"\n📄 Relatórios gerados em {REPORT_FILE}")

if __name__ == "__main__":
    analyzer = ReactAnalyzer()
    exit_code = analyzer.scan_project()
    # Em CI, falha se houver críticos
    sys.exit(1 if exit_code > 0 else 0)
