
import os
import sys
import json
import ast
import argparse
import hashlib
import statistics
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple
from collections import deque

# ==============================================================================
# 🧠 OTIMIZADOR DE ALINHAMENTO v5.4 (Maintenance Awareness)
# ==============================================================================
# Autor: Optimus Architect
# Conformidade: RFC-002 (Journal), RFC-004 (Auto-Task)
# Novidades: Sugestão de Manutenção de Kernel, Modularização de Relatório.
# ==============================================================================

BASE_DIR = Path(".")
CONFIG_DIR = BASE_DIR / "config"
CACHE_FILE = CONFIG_DIR / ".optimizer_cache.json"
HISTORY_FILE = CONFIG_DIR / "optimizer_history.json"
KERNEL_LOG = BASE_DIR / "kernel_journal.jsonl"
TASKS_FILE = BASE_DIR / "docs" / "TASKS.md"
MASTER_SPEC = BASE_DIR / "docs" / "governance" / "HYPEROPTIMUS_MASTER_SPEC.md"
BACKUP_DIR = BASE_DIR / "backups"
CODE_ROOTS = ["app", "scripts"]

WEIGHTS = {
    "BACKLOG": 20, "CODE_AST": 25, "ARCH": 15,
    "STRUCTURE": 10, "DOCS": 10, "KERNEL": 10, "SNAPSHOT": 10
}

class Colors:
    HEADER, BLUE, CYAN, GREEN, YELLOW, RED, ENDC, BOLD = '\033[95m', '\033[94m', '\033[96m', '\033[92m', '\033[93m', '\033[91m', '\033[0m', '\033[1m'

class KernelAdapter:
    @staticmethod
    def log_event(score: int, mode: str):
        event = {
            "id": str(uuid.uuid4()), "timestamp": datetime.now().isoformat(),
            "session_id": "OPTIMIZER_SESSION", "actor": "OPTIMIZER",
            "module": "CORTEX", "event_type": "ALIGNMENT_CHECK",
            "severity": "INFO" if score >= 90 else "WARN" if score >= 70 else "ERROR",
            "payload": {"score": score, "mode": mode}
        }
        try:
            with open(KERNEL_LOG, "a", encoding="utf-8") as f: f.write(json.dumps(event) + "\n")
        except: pass

class ProjectGenomics:
    def __init__(self):
        self.smells, self.hotspots = [], []
        if not CONFIG_DIR.exists(): CONFIG_DIR.mkdir(parents=True)
        try:
            with open(CACHE_FILE, "r") as f: self.cache = json.load(f)
        except: self.cache = {}

    def calculate_complexity(self, node):
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With, ast.BoolOp)): complexity += 1
        return complexity

    def scan(self) -> Dict[str, Any]:
        total_files, error_files, total_complexity, backend_files = 0, 0, 0, []
        for root_dir in CODE_ROOTS:
            for path in Path(root_dir).rglob("*.py"):
                total_files += 1
                if "app/" in str(path).replace("\\", "/"): backend_files.append(path.name)
                try:
                    content = path.read_text(encoding="utf-8")
                    f_hash = hashlib.sha256(content.encode()).hexdigest()
                    if self.cache.get(str(path), {}).get("hash") == f_hash:
                        comp = self.cache[str(path)]["data"]["complexity"]
                        self.smells.extend(self.cache[str(path)]["data"].get("smells", []))
                    else:
                        tree = ast.parse(content)
                        comp = self.calculate_complexity(tree)
                        new_smells = []
                        if len(content.splitlines()) > 400: new_smells.append(f"Arquivo Gigante: {path}")
                        self.smells.extend(new_smells)
                        self.cache[str(path)] = {"hash": f_hash, "data": {"complexity": comp, "smells": new_smells}}
                    total_complexity += comp
                    if comp > 20: self.hotspots.append((str(path), comp))
                except SyntaxError: error_files += 1
                except: pass
        with open(CACHE_FILE, "w") as f: json.dump(self.cache, f)
        return {
            "quality_score": int(max(0, 100 - (error_files / total_files * 300))) if total_files else 0,
            "arch_score": max(0, 100 - len(self.smells)*5),
            "avg_complexity": total_complexity / total_files if total_files else 0,
            "hotspots": sorted(self.hotspots, key=lambda x: x[1], reverse=True)[:5],
            "smells": self.smells[:5]
        }

class AlignmentComputer:
    def compute(self):
        k_score, kernel_errors = 100, []
        if KERNEL_LOG.exists():
            with open(KERNEL_LOG, "r", encoding="utf-8") as f:
                for line in deque(f, maxlen=50):
                    try:
                        ev = json.loads(line)
                        if ev.get("severity") == "CRITICAL": k_score -= 10
                        elif ev.get("severity") == "ERROR": k_score -= 5
                        if ev.get("severity") in ["ERROR", "CRITICAL"]: kernel_errors.append(ev.get("event_type"))
                    except: continue
        stats = ProjectGenomics().scan()
        required = ["app/main.py", "atualizar.py", str(MASTER_SPEC)]
        s_score = int((sum(1 for f in required if os.path.exists(f)) / len(required)) * 100)
        open_tasks = [l for l in TASKS_FILE.read_text(encoding="utf-8").splitlines() if "- [ ]" in l] if TASKS_FILE.exists() else []
        b_score = max(0, 100 - len(open_tasks)*2)
        snap_score = 0
        if BACKUP_DIR.exists():
            snaps = sorted(list(BACKUP_DIR.glob("*.zip")))
            if snaps:
                age = (datetime.now() - datetime.fromtimestamp(snaps[-1].stat().st_mtime)).total_seconds() / 3600
                snap_score = 100 if age < 2 else 70 if age < 24 else 40
        final = sum(val * WEIGHTS[key] for key, val in {"BACKLOG": b_score, "CODE_AST": stats["quality_score"], "ARCH": stats["arch_score"], "STRUCTURE": s_score, "KERNEL": k_score, "SNAPSHOT": snap_score}.items()) / 100
        return {"total_score": int(final), "breakdown": {"Backlog": b_score, "Code": stats["quality_score"], "Arch": stats["arch_score"], "Structure": s_score, "Kernel": k_score, "Snapshot": snap_score}, "stats": stats, "open_tasks": open_tasks, "kernel_errors": list(set(kernel_errors))}

def print_report(data, auto_fix=False):
    score = data["total_score"]
    color = Colors.GREEN if score >= 90 else Colors.YELLOW if score >= 70 else Colors.RED
    print(f"\n{Colors.HEADER}🧬 MESAFLOW ALIGNMENT REPORT v8.2{Colors.ENDC}\n{'='*60}\nSCORE GLOBAL: {color}{score}/100{Colors.ENDC}\n{'-'*60}")
    for key, val in data["breakdown"].items():
        print(f"  {key:<10} | {val:>3} | {'█' * int(val // 10)}")
    if data["stats"]["smells"]:
        print(f"\n{Colors.YELLOW}⚠️  Architecture Smells:{Colors.ENDC}")
        for s in data["stats"]["smells"]: print(f"   - {s}")
    print(f"\n{Colors.BOLD}🚀 PLANO DE AÇÃO:{Colors.ENDC}")
    if score < 90:
        if data["stats"]["hotspots"] and auto_fix:
            target = data["stats"]["hotspots"][0][0]
            task = f"\n- [ ] **[AUTO-OPT | CODE | HIGH]** Refatorar {target}\n      Motivo: Complexidade {data['stats']['hotspots'][0][1]} excede limite.\n"
            with open(TASKS_FILE, "a", encoding="utf-8") as f: f.write(task)
            print(f"{Colors.GREEN}⚡ Task de Refatoração Criada.{Colors.ENDC}")
        if data["breakdown"]["Kernel"] < 60:
            print(f"{Colors.CYAN}💡 Sugestão: O Kernel Score está baixo devido a erros antigos. Considere limpar o 'kernel_journal.jsonl' se o sistema estiver estável.{Colors.ENDC}")
        if data["open_tasks"]: print(f"1. Focar nas {len(data['open_tasks'])} tasks abertas.")
    else:
        print(f"{Colors.GREEN}>>> MODO EVOLUTIVO (OWNER MODE) <<<{Colors.ENDC}\nO sistema está pronto para expansão.\n\nCopie este prompt para iniciar a evolução:\n{'-'*60}\n<Schema_Mission version=\"3.0\" priority=\"HIGH\">\n    <Identity><Role>Optimus Architect (Evolution Mode)</Role></Identity>\n    <Objectives><Objective>Propor melhoria técnica ou de UX.</Objective></Objectives>\n</Schema_Mission>\n{'-'*60}")
    KernelAdapter.log_event(score, "AUTO_FIX" if auto_fix else "AUTO")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto-fix", action="store_true")
    args = parser.parse_args()
    print_report(AlignmentComputer().compute(), args.auto_fix)

