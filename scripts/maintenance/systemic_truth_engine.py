import os
import re
import sys
import io
import json
import hashlib
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Optional, Any, Union
from dataclasses import dataclass, asdict, field

# ==============================================================================
# 🧬 MESAFLOW PREDICTIVE TRUTH ENGINE v9.1 (Sovereign Edition)
# ==============================================================================
# Autoridade: MesaFlow Kernel
# Protocolo: INDA/1.2 | SGCS/3.1 (Predictive)
# Objetivo: Detectar apodrecimento estrutural e tendências de regressão.
# ==============================================================================

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROJECT_ROOT = Path(".")
EPISTEMIC_DIR = Path("governance/epistemic")
OUTPUT_JSON = "project-ai-context.json"
OUTPUT_MD = "project-ai-context.md"
OUTPUT_BUNDLE = "MESAFLOW_COGNITIVE_BUNDLE.txt"

IGNORE_DIRS = {"node_modules", ".next", ".git", ".vscode", "coverage", "dist", "build", "__pycache__", "public", "assets", ".venv", "venv", "ignorar", "backups"}
TARGET_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".py"}

@dataclass
class FalsificationExperiment:
    id: str
    hypothesis: str
    method: str 
    result: str = "PENDING"
    impact_delta: float = 0.0

@dataclass
class Responsibility:
    fact: str
    hypothesis: str
    inference: str
    confidence: str
    falsifiable_by: List[FalsificationExperiment]

@dataclass
class FileTruth:
    path: str
    layer: str
    responsibility: Responsibility
    lines: int
    hash_secure: str
    blast_radius: float = 0.0
    issues: List[Dict] = field(default_factory=list)

class EpistemicLaboratory:
    def __init__(self):
        self.file_map: Dict[str, FileTruth] = {}
        self.history: List[Dict] = []
        self.stats = {
            "files": 0, "lines": 0, "critical_issues": 0, 
            "start_time": time.time(), "version": "9.1.0",
            "worst_case_confidence": 1.0,
            "confidence_delta": 0.0,
            "dominant_model": "STRICT_LAYERING"
        }
        self._setup_dirs()

    def _setup_dirs(self):
        for d in ["models", "experiments", "history", "overrides"]:
            (EPISTEMIC_DIR / d).mkdir(parents=True, exist_ok=True)

    def load_history(self):
        history_path = EPISTEMIC_DIR / "history/epistemic_series.json"
        if history_path.exists():
            try:
                self.history = json.loads(history_path.read_text())
            except: self.history = []

    def infer_responsibility(self, content: str, path: str, ext: str) -> Responsibility:
        has_jsx = bool(re.search(r'<[A-Z][\w\.]+(?:\s|/|>)', content)) if ext in [".tsx", ".jsx"] else False
        has_data = bool(re.search(r'fetch\(|axios\.|useSWR|useQuery', content))
        
        exp = FalsificationExperiment(
            id=f"EXP-{hashlib.md5(path.encode()).hexdigest()[:4]}",
            hypothesis="Se removermos o JSX, o arquivo torna-se um Service puro?",
            method="VIRTUAL_STRESS"
        )

        if has_jsx and has_data:
            return Responsibility("HAS_JSX && HAS_DATA", "UI_E_DATA_MISTURADOS", "GOD_OBJECT", "CERTAIN", [exp])
        if has_jsx:
            return Responsibility("HAS_JSX", "UI_COMPONENT", "UI_RENDER", "HIGH", [exp])
        
        return Responsibility("NO_MARKERS", "LOGICA_PURA", "PURE_LOGIC", "LOW", [])

    def analyze_file(self, path: Path):
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            secure_hash = hashlib.sha256(f"{path}:{content}".encode()).hexdigest()[:16]
        except: return
        rel_path = str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
        layer = self.get_layer(rel_path)
        self.file_map[rel_path] = FileTruth(
            path=rel_path, layer=layer,
            responsibility=self.infer_responsibility(content, rel_path, path.suffix),
            lines=len(content.splitlines()), hash_secure=secure_hash
        )
        self.file_map[rel_path]._raw_imports = [i for sub in re.findall(r'from\s+[\'"](.*?)[\'"]|import\([\'"](.*?)[\'"]\)', content) for i in sub if i]
        self.stats["files"] += 1

    def get_layer(self, path: str) -> str:
        if "frontend/src/app" in path: return "frontend_app"
        if "mobile/src" in path: return "mobile"
        for layer in ["components", "context", "hooks", "services", "lib", "types"]:
            if f"/{layer}/" in f"/{path}/": return layer
        return "unknown"

    def calculate_trends(self):
        """Analisa a variação de confiança entre ritos (Nível 9.1)."""
        if not self.history: return
        
        last_snapshot = self.history[-1]
        prev_confidence = last_snapshot.get("worst_confidence", 1.0)
        self.stats["confidence_delta"] = round(self.stats["worst_case_confidence"] - prev_confidence, 4)
        
        # Seleção de Modelo Dominante
        god_objects = len([f for f in self.file_map.values() if f.responsibility.inference == "GOD_OBJECT"])
        if god_objects > 5:
            self.stats["dominant_model"] = "STRICT_LAYERING"
        else:
            self.stats["dominant_model"] = "DOMAIN_DRIVEN"

    def generate_reports(self):
        # Blast Radius Ponderado
        LAYER_WEIGHTS = {"types": 2.5, "lib": 2.0, "services": 1.8, "context": 1.5}
        conf_values = []
        for path, meta in self.file_map.items():
            meta.blast_radius = round(len([p for p, m in self.file_map.items() if path in getattr(m, '_raw_imports', [])]) * LAYER_WEIGHTS.get(meta.layer, 1.0), 2)
            conf_map = {"CERTAIN": 1.0, "HIGH": 0.8, "MEDIUM": 0.5, "LOW": 0.2}
            conf_values.append(conf_map[meta.responsibility.confidence])
        
        self.stats["worst_case_confidence"] = min(conf_values) if conf_values else 0.0
        self.calculate_trends()

        # Snapshot
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "files": self.stats["files"],
            "worst_confidence": self.stats["worst_case_confidence"],
            "confidence_delta": self.stats["confidence_delta"]
        }
        self.history.append(snapshot)
        (EPISTEMIC_DIR / "history/epistemic_series.json").write_text(json.dumps(self.history, indent=2))

        # JSON
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump({
                "protocol": "SGCS/3.1",
                "verdict": "SYSTEM_OPERATIONAL" if self.stats["confidence_delta"] >= -0.05 else "PREDICTIVE_REGRESSION",
                "stats": self.stats,
                "history": self.history[-10:],
                "files": {p: asdict(m) for p, m in self.file_map.items()}
            }, f, indent=2)

    def generate_bundle(self):
        print(f"📦 Gerando Bundle Preditivo v9.1...")
        with open(OUTPUT_BUNDLE, "w", encoding="utf-8") as b:
            b.write("<MESAFLOW_EPISTEMIC_CONTRACT>\n")
            b.write(f"DOMINANT_MODEL={self.stats['dominant_model']}\n")
            b.write(f"CONFIDENCE_TREND={self.stats['confidence_delta']}\n")
            b.write("MANDATORY_BEHAVIOR=ANALYZE_TRENDS,CITE_FACTS,DECLARE_MODEL\n")
            b.write("</MESAFLOW_EPISTEMIC_CONTRACT>\n\n")
            
            for f_path, label in [
                ("governance/prompts/AI_SYSTEM_INITIATION.xml", "DNA & CONSTITUTION"),
                (OUTPUT_JSON, "STRUCTURAL_TRUTH_AND_TRENDS"),
                (OUTPUT_MD, "EXECUTIVE_SUMMARY")
            ]:
                p = Path(f_path)
                if p.exists():
                    b.write(f"[[MESAFLOW_BEGIN:{f_path}]]\n# LABEL: {label}\n")
                    b.write(p.read_text(encoding="utf-8", errors="ignore"))
                    b.write(f"\n[[MESAFLOW_END]]\n\n")

    def run(self):
        print(f"🚀 Iniciando Predictive Truth Engine v9.1...")
        self.load_history()
        for root, _, files in os.walk("."):
            if any(p in IGNORE_DIRS for p in Path(root).parts): continue
            for file in files:
                p = Path(root) / file
                if p.suffix in TARGET_EXTENSIONS: self.analyze_file(p)
        
        self.generate_reports()
        self.generate_bundle()
        
        if self.stats["confidence_delta"] < -0.1:
            print(f"❌ EPISTEMIC REGRESSION: Confidence dropped by {self.stats['confidence_delta']}")
            sys.exit(1)
        print(f"✅ Veredito: {self.stats['dominant_model']} ACTIVE")
        print(f"✅ Processo concluído. Bundle pronto em: {os.path.abspath(OUTPUT_BUNDLE)}")

if __name__ == "__main__":
    EpistemicLaboratory().run()