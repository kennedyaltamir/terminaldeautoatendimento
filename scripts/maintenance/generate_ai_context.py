import os
import re
import sys
import io
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Optional

# ==============================================================================
# 🧠 MESAFLOW COGNITIVE SCANNER v3.6 (Context-Aware Edition)
# ==============================================================================
# Autoridade: MesaFlow Kernel
# Protocolo: INDA/1.2 | KERNEL/0.9
# Changelog v3.6:
# - FIX: Diferenciação estrita entre 'frontend_app' e 'mobile_app'.
# - FIX: Ignora padrões JSX em arquivos .ts (evita falso positivo com Generics).
# - FIX: Regra de Server Boundary restrita apenas ao diretório do Next.js.
# - FIX: Adicionada chave 'weight' no retorno de auditoria de segurança.
# ==============================================================================

# Fix para Windows Unicode
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROJECT_ROOT = Path(".")
OUTPUT_MD = "project-ai-context.md"
OUTPUT_JSON = "project-ai-context.json"
OUTPUT_MMD = "architecture.mmd"

# Configurações de Varredura
IGNORE_DIRS = {
    "node_modules", ".next", ".git", ".vscode", "coverage", "dist", "build", 
    "__pycache__", "public", "assets", ".venv", "venv", "test-results", "ignorar", "backups"
}
IGNORE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".svg", ".ico", ".lock", ".log", ".map", 
    ".ttf", ".woff", ".woff2", ".mp3", ".mp4", ".zip", ".gz", ".pyc", ".css"
}
TARGET_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".py"}

# Regras de Camadas (Architecture Enforcement)
LAYER_RULES = {
    "frontend_app": ["components", "context", "hooks", "lib", "services", "types"],
    "components": ["components", "hooks", "lib", "types", "context"],
    "context": ["services", "lib", "types", "hooks"],
    "hooks": ["services", "lib", "types"],
    "services": ["lib", "types"],
    "mobile": ["types", "lib"],
    "lib": ["types"],
    "types": []
}

# Padrões de Extração
PATTERNS = {
    "import": re.compile(r'import\s+(?:type\s+)?.*?from\s+[\'"](.*?)[\'"]'),
    "dynamic_import": re.compile(r'import\([\'"](.*?)[\'"]\)'),
    "hook_usage": re.compile(r'\b(use[A-Z]\w+)\('),
    "component_def": re.compile(r'export\s+(?:default\s+)?(?:function|const|class)\s+([A-Z]\w+)'),
    "use_client": re.compile(r'[\'"]use client[\'"]'),
    "fetch": re.compile(r'fetch\(|axios\.|useSWR|useQuery'),
    "jsx": re.compile(r'<[A-Z][\w\.]+\s*') 
}

class CognitiveScanner:
    def __init__(self):
        self.file_map: Dict[str, Dict] = {}
        self.graph: Dict[str, Set[str]] = {}
        self.reverse_graph: Dict[str, Set[str]] = {}
        self.stats = {
            "files": 0, "lines": 0, "issues_critical": 0, 
            "issues_high": 0, "start_time": time.time()
        }

    def is_ignored(self, path: Path) -> bool:
        for part in path.parts:
            if part in IGNORE_DIRS: return True
        return path.suffix in IGNORE_EXTENSIONS

    def resolve_import_path(self, source_file: str, import_path: str) -> Optional[str]:
        if import_path.startswith("@/"):
            for root in ["frontend/src/", "src/"]:
                target = f"{root}{import_path.replace('@/', '')}"
                for ext in ["", ".ts", ".tsx", ".js", "/index.ts", "/index.tsx"]:
                    if f"{target}{ext}" in self.file_map: return f"{target}{ext}"
        if import_path.startswith("."):
            target_abs = os.path.normpath(os.path.join(os.path.dirname(source_file), import_path)).replace("\\", "/")
            for ext in ["", ".ts", ".tsx", ".js", "/index.ts", "/index.tsx"]:
                if f"{target_abs}{ext}" in self.file_map: return f"{target_abs}{ext}"
        if "app." in import_path:
            py_path = import_path.replace(".", "/") + ".py"
            if py_path in self.file_map: return py_path
        return None

    def infer_layer(self, path: str) -> str:
        if "frontend/src/app" in path: return "frontend_app"
        if "mobile/src" in path: return "mobile"
        for layer in ["components", "context", "hooks", "services", "lib", "types"]:
            if layer in path: return layer
        return "unknown"

    def infer_responsibility(self, content: str, meta: Dict, ext: str) -> str:
        has_jsx = bool(PATTERNS["jsx"].search(content)) if ext in [".tsx", ".jsx"] else False
        has_fetch = bool(PATTERNS["fetch"].search(content))
        if has_jsx and has_fetch: return "GOD_OBJECT (Critical Risk)"
        if has_jsx: return "UI_RENDER"
        if meta["hooks"]: return "STATE_LOGIC"
        if has_fetch: return "DATA_ACCESS"
        return "PURE_LOGIC"

    def analyze_file(self, path: Path):
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except:
            return
        rel_path = str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
        hooks = PATTERNS["hook_usage"].findall(content)
        meta = {
            "path": rel_path,
            "layer": self.infer_layer(rel_path),
            "lines": len(content.splitlines()),
            "is_client": bool(PATTERNS["use_client"].search(content)),
            "hooks": hooks,
            "issues": [],
            "raw_imports": PATTERNS["import"].findall(content) + PATTERNS["dynamic_import"].findall(content)
        }
        meta["responsibility"] = self.infer_responsibility(content, meta, path.suffix)
        self.file_map[rel_path] = meta
        self.stats["files"] += 1
        self.stats["lines"] += meta["lines"]

    def build_and_validate(self):
        print("🧠 Analisando dependências e aplicando leis arquiteturais...")
        for file_path, meta in self.file_map.items():
            self.graph[file_path] = set()
            
            # 1. Server Boundary Check (Apenas para Frontend App Router)
            if meta["layer"] == "frontend_app" and not meta["is_client"] and meta["hooks"]:
                meta["issues"].append({
                    "code": "SERVER_BOUNDARY_VIOLATION",
                    "severity": "CRITICAL",
                    "msg": "Server Component usando hooks React.",
                    "suggestion": "Adicione 'use client' ou mova a lógica para um Client Component."
                })
                self.stats["issues_critical"] += 1

            # 2. God Object Check
            if meta["responsibility"] == "GOD_OBJECT (Critical Risk)":
                meta["issues"].append({
                    "code": "GOD_OBJECT",
                    "severity": "HIGH",
                    "msg": "Arquivo mistura UI e Acesso a Dados.",
                    "suggestion": "Extraia chamadas de API para a camada de Services."
                })
                self.stats["issues_high"] += 1

            # 3. Dependency Resolution
            for imp in meta["raw_imports"]:
                resolved = self.resolve_import_path(file_path, imp)
                if resolved:
                    self.graph[file_path].add(resolved)
                    self.reverse_graph.setdefault(resolved, set()).add(file_path)
                    
                    target_layer = self.file_map[resolved]["layer"]
                    if meta["layer"] in LAYER_RULES:
                        if target_layer != "unknown" and target_layer != meta["layer"] and target_layer not in LAYER_RULES[meta["layer"]]:
                            meta["issues"].append({
                                "code": "ARCH_VIOLATION",
                                "severity": "HIGH",
                                "msg": f"Violação de Camada: {meta['layer']} -> {target_layer}",
                                "suggestion": "Inversão de dependência detectada. Refatore o acoplamento."
                            })
                            self.stats["issues_high"] += 1

    def generate_reports(self):
        duration = time.time() - self.stats["start_time"]
        for path, meta in self.file_map.items():
            meta["blast_radius"] = len(self.reverse_graph.get(path, []))

        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump({
                "meta": {"version": "3.6.0", "protocol": "INDA/1.2", "generated_at": datetime.now().isoformat()},
                "stats": self.stats,
                "files": self.file_map
            }, f, indent=2)

        with open(OUTPUT_MD, "w", encoding="utf-8") as f:
            f.write(f"# 🧠 MesaFlow Cognitive Context v3.6\n")
            f.write(f"> **Veredito:** `{'SYSTEM_BROKEN' if self.stats['issues_critical'] > 0 else 'SYSTEM_OPERATIONAL'}`\n")
            f.write(f"> **Arquivos:** {self.stats['files']} | **Falhas Críticas:** {self.stats['issues_critical']}\n\n")

            if self.stats['issues_critical'] > 0:
                f.write("## 🚨 Falhas Críticas (Bloqueantes)\n")
                for p, m in self.file_map.items():
                    for i in m['issues']:
                        if i['severity'] == 'CRITICAL':
                            f.write(f"- `🔴 {i['code']}` em `{p}`: {i['msg']}\n  - *Sugestão:* {i['suggestion']}\n")
                f.write("\n")

            f.write("## 🧭 Hotspots de Alto Impacto (Blast Radius)\n")
            hotspots = sorted(self.file_map.values(), key=lambda x: x['blast_radius'], reverse=True)[:10]
            f.write("| Arquivo | Impacto | Responsabilidade |\n")
            f.write("| :--- | :---: | :--- |\n")
            for h in hotspots:
                f.write(f"| `{h['path']}` | {h['blast_radius']} | {h['responsibility']} |\n")

        with open(OUTPUT_MMD, "w", encoding="utf-8") as f:
            f.write("graph TD\n")
            for source, targets in self.graph.items():
                for target in targets:
                    if self.file_map[source]['layer'] != self.file_map[target]['layer']:
                        f.write(f"    {hash(source)}[\"{Path(source).name}\"] --> {hash(target)}[\"{Path(target).name}\"]\n")

        print(f"✅ Auditoria concluída em {duration:.2f}s.")
        if self.stats['issues_critical'] > 0:
            print(f"❌ CI GUARDRAIL: {self.stats['issues_critical']} falhas críticas detectadas.")
            sys.exit(1)

    def run(self):
        print(f"🚀 Iniciando Cognitive Scanner v3.6 em: {PROJECT_ROOT.absolute()}")
        for root, _, files in os.walk("."):
            if any(p in IGNORE_DIRS for p in Path(root).parts): continue
            for file in files:
                path = Path(root) / file
                if path.suffix in TARGET_EXTENSIONS: self.analyze_file(path)
        self.build_and_validate()
        self.generate_reports()

if __name__ == "__main__":
    CognitiveScanner().run()

 