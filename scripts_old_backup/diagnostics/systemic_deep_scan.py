# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 21:15:00
import os
import sys
import json
import re
import subprocess
import io
from pathlib import Path
from typing import Dict, List, Any

# Hardening para Windows (UTF-8 Enforcement)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==============================================================================
# 🩺 MESAFLOW SYSTEMIC DEEP SCAN (L2 DIAGNOSTIC)
# ==============================================================================
# Objetivo: Análise estática e dinâmica profunda para correlação de erros L0.
# Não corrige. Apenas aponta a verdade técnica com precisão cirúrgica.
# ==============================================================================

class SystemicDeepScanner:
    def __init__(self):
        self.root = Path(".")
        self.report = {
            "timestamp": "",
            "l0_status": "UNKNOWN",
            "build_config": {},
            "contract_violations": [],
            "async_safety": [],
            "file_integrity": []
        }
        self.frontend_dir = self.root / "frontend"

    def _read_file(self, path: Path) -> str:
        if not path.exists():
            return ""
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            return ""

    def run_l0_probe(self):
        """Executa a verdade física (TSC)."""
        print("🔍 [L0] Sondando Realidade Física (TypeScript)...")
        try:
            # Executa tsc apenas para checagem de tipos
            result = subprocess.run(
                "npx tsc --noEmit",
                cwd=self.frontend_dir,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            self.report["l0_status"] = "PASS" if result.returncode == 0 else "FAIL"
            
            if result.returncode != 0:
                # Parsear erros para identificar arquivos quentes
                errors = result.stdout.splitlines()
                parsed_errors = []
                for line in errors:
                    if "error TS" in line:
                        # Extrai arquivo e linha (ex: src/components/menu/MenuClient.tsx(187,9))
                        match = re.search(r'([a-zA-Z0-9_/.-]+\.tsx?)\((\d+),\d+\): error (TS\d+): (.+)', line)
                        if match:
                            parsed_errors.append({
                                "file": match.group(1),
                                "line": match.group(2),
                                "code": match.group(3),
                                "message": match.group(4)
                            })
                self.report["l0_errors"] = parsed_errors
                print(f"   ❌ TSC Falhou com {len(parsed_errors)} erros estruturados.")
        except Exception as e:
            self.report["l0_status"] = "CRASH"
            self.report["l0_crash_reason"] = str(e)
            print(f"   💥 Falha na execução do TSC: {e}")

    def audit_tsconfig_integrity(self):
        """Verifica se o tsconfig aponta para fantasmas."""
        print("🔍 [CFG] Auditando Configuração de Build...")
        tsconfig_path = self.frontend_dir / "tsconfig.json"
        if not tsconfig_path.exists():
            self.report["build_config"]["status"] = "MISSING"
            return

        try:
            config = json.loads(self._read_file(tsconfig_path))
            includes = config.get("include", [])
            
            ghost_paths = []
            for pattern in includes:
                # Simplificação: verifica apenas caminhos diretos, não globs complexos
                clean_path = pattern.replace("/**/*.ts", "").replace("/**/*.tsx", "")
                if "*" not in clean_path:
                    full_path = self.frontend_dir / clean_path
                    if not full_path.exists():
                        ghost_paths.append(clean_path)
            
            # Verifica .next/types
            next_types = self.frontend_dir / ".next" / "types"
            
            self.report["build_config"] = {
                "status": "ANALYZED",
                "ghost_includes": ghost_paths,
                "next_types_exists": next_types.exists(),
                "strict_mode": config.get("compilerOptions", {}).get("strict", False)
            }
            
            if ghost_paths:
                print(f"   ⚠️  Caminhos fantasmas no tsconfig: {ghost_paths}")
            if not next_types.exists():
                print("   ⚠️  Tipos do Next.js (.next/types) não encontrados. Build pode estar stale.")

        except Exception as e:
            self.report["build_config"]["error"] = str(e)

    def analyze_component_contracts(self):
        """
        Análise Estática Profunda de Contratos (Props e Funções).
        Foco: MenuClient.tsx vs SplitBillModal.tsx vs CartContext.tsx
        """
        print("🔍 [AST] Analisando Contratos de Componentes...")
        
        # 1. Analisar Definição do SplitBillModal
        modal_path = self.frontend_dir / "src/components/menu/SplitBillModal.tsx"
        modal_props = []
        if modal_path.exists():
            content = self._read_file(modal_path)
            # Regex heurística para extrair interface Props
            match = re.search(r'interface\s+SplitBillModalProps\s+{([^}]+)}', content, re.DOTALL)
            if match:
                props_block = match.group(1)
                # Extrai nomes das props
                modal_props = re.findall(r'(\w+)\??:', props_block)
        
        # 2. Analisar Definição do CartContext (addToCart)
        cart_path = self.frontend_dir / "src/context/CartContext.tsx"
        add_to_cart_sig = "UNKNOWN"
        if cart_path.exists():
            content = self._read_file(cart_path)
            # Procura a assinatura na interface
            match = re.search(r'addToCart:\s*\(([^)]+)\)\s*=>', content)
            if match:
                add_to_cart_sig = match.group(1) # ex: product: Product, quantity: number...

        # 3. Analisar Uso no MenuClient
        client_path = self.frontend_dir / "src/components/menu/MenuClient.tsx"
        if client_path.exists():
            content = self._read_file(client_path)
            
            # Check 1: Uso do SplitBillModal
            # Procura <SplitBillModal ... /> e extrai as props passadas
            modal_usage = re.search(r'<SplitBillModal\s+([^>]+)/>', content, re.DOTALL)
            if modal_usage:
                usage_str = modal_usage.group(1)
                used_props = re.findall(r'(\w+)=', usage_str)
                
                # Diff
                extra_props = [p for p in used_props if p not in modal_props]
                missing_props = [p for p in modal_props if p not in used_props and "?" not in p] # Ignora opcionais na heurística simples
                
                if extra_props or missing_props:
                    self.report["contract_violations"].append({
                        "component": "SplitBillModal",
                        "defined_props": modal_props,
                        "used_props": used_props,
                        "extra_props_detected": extra_props,
                        "missing_props_detected": missing_props,
                        "verdict": "CONTRACT_BROKEN"
                    })
                    print(f"   ❌ Contrato Quebrado em SplitBillModal: Extras={extra_props}")

            # Check 2: Uso do addToCart
            # Procura chamadas addToCart(...)
            # Heurística: conta vírgulas dentro dos parênteses
            calls = re.findall(r'addToCart\(([^)]+)\)', content)
            for call_args in calls:
                arg_count = len(call_args.split(','))
                # Comparar com a definição (simplificado)
                expected_args = len(add_to_cart_sig.split(',')) if add_to_cart_sig != "UNKNOWN" else 0
                
                if add_to_cart_sig != "UNKNOWN" and arg_count != expected_args:
                     self.report["contract_violations"].append({
                        "function": "addToCart",
                        "expected_args_count": expected_args,
                        "found_args_count": arg_count,
                        "signature": add_to_cart_sig,
                        "verdict": "SIGNATURE_MISMATCH"
                    })
                     print(f"   ❌ Assinatura Incompatível em addToCart: Esperado {expected_args}, Encontrado {arg_count}")

    def analyze_python_async_safety(self):
        """Verifica se testes estão usando asyncio.run indevidamente."""
        print("🔍 [PY] Auditando Segurança Async (Python 3.13)...")
        scripts_dir = self.root / "scripts/automation"
        violations = []
        
        for path in scripts_dir.glob("test_*.py"):
            content = self._read_file(path)
            # Se usa pytest.mark.asyncio E asyncio.run, é violação
            if "@pytest.mark.asyncio" in content and "asyncio.run(" in content:
                violations.append(str(path))
        
        self.report["async_safety"] = {
            "violations": violations,
            "status": "FAIL" if violations else "PASS"
        }
        if violations:
            print(f"   ❌ Conflito de Loop detectado em: {violations}")

    def generate_final_report(self):
        output_path = self.root / "governance/evidence/SYSTEMIC_DEEP_SCAN.json"
        
        # Determina Veredito Final
        l0_fail = self.report["l0_status"] != "PASS"
        contract_fail = len(self.report["contract_violations"]) > 0
        async_fail = self.report["async_safety"]["status"] == "FAIL"
        
        if l0_fail or contract_fail or async_fail:
            self.report["final_verdict"] = "SYSTEM_BROKEN"
            self.report["action_plan"] = "REQUIRES_INTERVENTION"
        else:
            self.report["final_verdict"] = "SYSTEM_STABLE"
            self.report["action_plan"] = "NONE"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2)
            
        print("\n" + "="*60)
        print("📊 RELATÓRIO DE DIAGNÓSTICO SISTÊMICO")
        print("="*60)
        print(f"Veredito: {self.report['final_verdict']}")
        print(f"Erros L0 (TSC): {len(self.report.get('l0_errors', []))}")
        print(f"Violações de Contrato: {len(self.report['contract_violations'])}")
        print(f"Conflitos Async: {len(self.report['async_safety']['violations'])}")
        print(f"Arquivo: {output_path}")
        print("="*60)

    def run(self):
        print("🚀 Iniciando Deep Scan...")
        self.run_l0_probe()
        self.audit_tsconfig_integrity()
        self.analyze_component_contracts()
        self.analyze_python_async_safety()
        self.generate_final_report()

if __name__ == "__main__":
    scanner = SystemicDeepScanner()
    scanner.run()

