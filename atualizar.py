# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 23:50:00
import os
import shutil
import re
import sys
import json
import hashlib
import ast
import zipfile
import uuid
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime

# ==============================================================================
# 🧬 MESAFLOW KERNEL EXECUTOR v8.3 (Strict-Learning)
# ==============================================================================
# Autor: Optimus Architect
# Protocolo: INDA Strict (RFC-001 a RFC-007 Compliant)
# Mudanças v8.3:
# - ENFORCEMENT: Bloqueio de execução se <Knowledge_Accumulation> estiver ausente.
# ==============================================================================

INPUT_FILE = "resposta.txt"
BACKUP_ROOT = Path("backups")
JOURNAL_FILE = "kernel_journal.jsonl"
STAGING_ROOT = Path("ignorar/diff_staging")
KNOWLEDGE_BASE_FILE = Path("docs/technical/AI_KNOWLEDGE_BASE.md")

# RFC-007: Security Boundary
PROTECTED_FILES = {
    ".env", ".gitignore", "atualizar.py", "gerartxt.py", "register.tsx",
    "package-lock.json", "yarn.lock"
}
PROTECTED_DIRECTORIES = ["docs/governance"]

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class IndaPhase(Enum):
    BOOT = "BOOT"
    RECEIVE = "RECEIVE"
    ANALYZE = "ANALYZE"
    PLAN = "PLAN"
    APPLY = "APPLY"
    VERIFY = "VERIFY"
    REPORT = "REPORT"

# --- 1. KERNEL SUPERVISOR (RFC-002) ---

class MesaFlowKernel:
    def __init__(self):
        self.session_id = str(uuid.uuid4())[:8]
        self.phase = IndaPhase.BOOT
        self.metrics = {"files": 0, "lines": 0, "complexity": 0, "risk": 0}

    def set_phase(self, phase: IndaPhase):
        self.phase = phase
        print(f"{Colors.BLUE}🔄 KERNEL PHASE: {phase.value}{Colors.ENDC}")

    def log(self, event_type: str, payload: Dict, severity: str = "INFO"):
        """Implementa o RFC-002: Kernel Journal Schema"""
        event = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "actor": "SYSTEM",
            "module": "KERNEL",
            "event_type": event_type,
            "severity": severity,
            "payload": payload
        }
        try:
            with open(JOURNAL_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(event) + "\n")
        except: pass

    def check_permission(self, path: Path, raw_content: str) -> bool:
        """Implementa RFC-006 e RFC-007"""
        path_str = str(path).replace("\\", "/")
        if ".." in path_str or path_str.startswith("/"): return False
        
        is_protected = path.name in PROTECTED_FILES or any(path_str.startswith(d) for d in PROTECTED_DIRECTORIES)
        
        if is_protected:
            return "<Governance_Override>" in raw_content
        return True

# --- 2. HYPER OPTIMUS AGENT (Cognitive Auditor) ---

class HyperOptimusAgent:
    @staticmethod
    def audit_code(path: Path, code: str) -> Dict[str, Any]:
        analysis = {"valid": True, "issues": [], "complexity": 0}
        
        if path.suffix == ".py":
            try:
                tree = ast.parse(code)
                analysis["complexity"] = len([n for n in ast.walk(tree)])
            except SyntaxError as e:
                analysis["valid"] = False
                analysis["issues"].append(f"Sintaxe Inválida: {e.msg} (Linha {e.lineno})")

        # Validação de Placeholders (FFP-02) com Inteligência de Caminho
        omission_indicators = [
            r"restante do código", 
            r"code omitted",
            r"(?m)^\s*(#|//)?\s*\.\.\.\s*$" 
        ]
        
        for pattern in omission_indicators:
            if re.search(pattern, code, re.IGNORECASE):
                analysis["issues"].append(f"Omissão detectada: '{pattern}'")
                analysis["valid"] = False
        
        return analysis

# --- 3. TRANSACTION MANAGER (RFC-005 & Atomic Swap) ---

class TransactionManager:
    def __init__(self, kernel: MesaFlowKernel):
        self.kernel = kernel
        self.backup_zip = None

    def create_targeted_snapshot(self, file_paths: List[Path]):
        """RFC-005: Backup apenas dos arquivos que serão tocados."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_zip = BACKUP_ROOT / f"transaction_{ts}_{self.kernel.session_id}.zip"
        BACKUP_ROOT.mkdir(exist_ok=True)
        
        print(f"{Colors.CYAN}📸 [RFC-005] Criando snapshot dos arquivos afetados...{Colors.ENDC}")
        count = 0
        try:
            with zipfile.ZipFile(self.backup_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for path in file_paths:
                    if path.exists() and path.is_file():
                        zipf.write(path, str(path))
                        count += 1
            self.kernel.log("SNAPSHOT_CREATED", {"path": str(self.backup_zip), "files": count})
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️  Falha no Snapshot: {e}{Colors.ENDC}")

    def atomic_write(self, path: Path, content: str) -> bool:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            temp_file = path.with_suffix(".tmp")
            temp_file.write_text(content + "\n", encoding="utf-8")
            
            mem_hash = hashlib.sha256(content.strip().encode()).hexdigest()
            disk_hash = hashlib.sha256(temp_file.read_text(encoding="utf-8").strip().encode()).hexdigest()
            
            if mem_hash != disk_hash:
                raise IOError(f"Falha de integridade (Hash Mismatch) em {path}")
            
            if path.exists(): os.remove(path)
            os.rename(temp_file, path)
            return True
        except Exception as e:
            print(f"{Colors.RED}❌ Erro de I/O em {path}: {e}{Colors.ENDC}")
            return False

# --- 4. DIFF & STAGING MANAGER (Safe Mode) ---

def open_diff_tool(original, proposed):
    """Tenta abrir o VS Code em modo diff."""
    try:
        subprocess.Popen(f"code --diff \"{original}\" \"{proposed}\"", shell=True)
        return True
    except Exception as e:
        print(f"{Colors.YELLOW}⚠️  Não foi possível abrir o VS Code automaticamente: {e}{Colors.ENDC}")
        return False

def ensure_dir(file_path):
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

# --- 5. KNOWLEDGE ACCUMULATOR ---

def accumulate_knowledge(raw_content: str) -> bool:
    """Extrai e anexa conhecimento à base técnica. Retorna True se encontrou."""
    match = re.search(r"<Knowledge_Accumulation>(.*?)</Knowledge_Accumulation>", raw_content, re.DOTALL)
    if match:
        content = match.group(1).strip()
        # Limpeza de CDATA se presente
        content = content.replace("<![CDATA[", "").replace("]]>", "").strip()
        
        if content:
            KNOWLEDGE_BASE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(KNOWLEDGE_BASE_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n\n--- ENTRY: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
                f.write(content)
            print(f"   🧠 {Colors.CYAN}Conhecimento acumulado em {KNOWLEDGE_BASE_FILE}{Colors.ENDC}")
            return True
    return False

# --- 6. PIPELINE PRINCIPAL ---

def main():
    kernel = MesaFlowKernel()
    agent = HyperOptimusAgent()
    tm = TransactionManager(kernel)

    print(f"{Colors.HEADER}🧬 MESAFLOW KERNEL EXECUTOR v8.3 (Strict-Learning){Colors.ENDC}")
    
    kernel.set_phase(IndaPhase.RECEIVE)
    input_p = Path(INPUT_FILE)
    if not input_p.exists():
        print(f"{Colors.RED}❌ Input {INPUT_FILE} não encontrado.{Colors.ENDC}")
        return

    try:
        raw_content = input_p.read_text(encoding="utf-8").strip()
    except UnicodeDecodeError:
        raw_content = input_p.read_text(encoding="latin-1").strip()

    # Processa Conhecimento antes dos arquivos
    # ENFORCEMENT: Bloqueia se não houver aprendizado
    if not accumulate_knowledge(raw_content):
        print(f"\n{Colors.RED}🛑 BLOQUEIO DE PROTOCOLO (L6){Colors.ENDC}")
        print(f"   A resposta da IA foi rejeitada pois não contém o bloco {Colors.BOLD}<Knowledge_Accumulation>{Colors.ENDC}.")
        print(f"   Toda interação deve gerar aprendizado persistente para evitar estagnação.")
        print(f"   Adicione o bloco e tente novamente.")
        return

    blocks = re.findall(r"\[\[MESAFLOW_BEGIN:(.*?)\]\](.*?)\[\[MESAFLOW_END\]\]", raw_content, re.DOTALL)

    if not blocks:
        print(f"{Colors.YELLOW}⚠️  Nenhum bloco de arquivo detectado.{Colors.ENDC}")
        return

    kernel.set_phase(IndaPhase.ANALYZE)
    files_to_process = []
    
    # Prepara diretório de staging
    run_id = datetime.now().strftime("%H%M%S")
    run_staging_dir = STAGING_ROOT / run_id
    run_staging_dir.mkdir(parents=True, exist_ok=True)

    for path_str, code in blocks:
        path = Path(path_str.strip())
        
        # Remove primeira quebra de linha se existir (artefato do regex)
        if code.startswith("\n"):
            code = code[1:]

        if not kernel.check_permission(path, raw_content):
            print(f"   🚫 {Colors.RED}BLOQUEADO: {path} (Sem Override){Colors.ENDC}")
            kernel.log("SECURITY_BLOCK", {"path": str(path)}, "CRITICAL")
            continue

        analysis = agent.audit_code(path, code)
        if not analysis["valid"]:
            print(f"   ❌ {Colors.RED}REJEITADO: {path}{Colors.ENDC}")
            for issue in analysis["issues"]: print(f"      - {issue}")
            continue

        files_to_process.append({"path": path, "code": code, "complexity": analysis["complexity"]})
        print(f"   ✅ ANALISADO: {path} (Carga: {analysis['complexity']})")

    if not files_to_process:
        print("🚫 Nenhum arquivo apto para aplicação.")
        return

    kernel.set_phase(IndaPhase.PLAN)
    
    # Loop de Confirmação Manual
    success_count = 0
    tm.create_targeted_snapshot([f["path"] for f in files_to_process])

    for item in files_to_process:
        target_path = item["path"]
        code = item["code"]
        staged_path = run_staging_dir / target_path
        
        ensure_dir(staged_path)
        with open(staged_path, "w", encoding="utf-8") as f:
            f.write(code)

        print(f"\n--------------------------------------------------")
        print(f"📄 Alvo: {Colors.BOLD}{target_path}{Colors.ENDC}")

        if target_path.exists():
            print(f"   🔍 Abrindo Diff Visual...")
            open_diff_tool(target_path.resolve(), staged_path.resolve())
            
            while True:
                choice = input(f"{Colors.YELLOW}   👉 Aplicar alteração? [y/n/c(cancel)]: {Colors.ENDC}").lower().strip()
                if choice == 'y':
                    if tm.atomic_write(target_path, code):
                        print(f"   ✅ {Colors.GREEN}Atualizado.{Colors.ENDC}")
                        kernel.metrics["files"] += 1
                        kernel.metrics["lines"] += len(code.splitlines())
                        kernel.metrics["complexity"] += item["complexity"]
                        success_count += 1
                    break
                elif choice == 'n':
                    print(f"   🚫 {Colors.RED}Ignorado. (Cópia salva em {staged_path}){Colors.ENDC}")
                    break
                elif choice == 'c':
                    print(f"   🛑 {Colors.RED}Operação cancelada pelo usuário.{Colors.ENDC}")
                    sys.exit(0)
        else:
            print(f"   ✨ {Colors.GREEN}Novo Arquivo Detectado.{Colors.ENDC}")
            subprocess.Popen(f"code \"{staged_path}\"", shell=True)
            
            while True:
                choice = input(f"{Colors.YELLOW}   👉 Criar arquivo? [y/n]: {Colors.ENDC}").lower().strip()
                if choice == 'y':
                    if tm.atomic_write(target_path, code):
                        print(f"   ✅ {Colors.GREEN}Criado.{Colors.ENDC}")
                        kernel.metrics["files"] += 1
                        kernel.metrics["lines"] += len(code.splitlines())
                        kernel.metrics["complexity"] += item["complexity"]
                        success_count += 1
                    break
                elif choice == 'n':
                    print(f"   🚫 {Colors.RED}Ignorado.{Colors.ENDC}")
                    break

    kernel.set_phase(IndaPhase.REPORT)
    kernel.log("EXECUTION_SUCCESS", kernel.metrics)
    
    print("\n" + "="*60)
    print(f"📊 RELATÓRIO DE INTELIGÊNCIA (Nível 4)")
    print(f"   Sessão: {kernel.session_id} | Status: {Colors.GREEN}ESTÁVEL{Colors.ENDC}")
    print(f"   Arquivos Aplicados: {success_count} | Carga Cognitiva: {kernel.metrics['complexity']}")
    print("="*60)

if __name__ == "__main__":
    main()