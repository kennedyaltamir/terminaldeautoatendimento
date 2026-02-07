# MESAFLOW OS - FRONTEND FORENSIC SCANNER
# Version: 1.1.1 (ASCII Purified)
# Objective: Map frontend entropy and prepare for correction rite.
# Invariants: Server is the Arbiter | Evidence First

import os
import subprocess
import json
import shutil
import re
from pathlib import Path
from datetime import datetime

class FrontendAuditor:
    def __init__(self):
        # Script must run at the project root
        self.root = Path("frontend")
        self.output_dir = Path("auditoria_frontend")
        self.folders = {
            "erros": self.output_dir / "erros",
            "corrigidos": self.output_dir / "corrigidos",
            "logs": self.output_dir / "logs"
        }
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "total_errors": 0,
            "files_affected": [],
            "details": []
        }

    def setup(self):
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        for folder in self.folders.values():
            folder.mkdir(parents=True, exist_ok=True)

    def run_tsc_audit(self):
        print("Scanning [1/3] Starting Type Audit (TSC)...")
        # Runs TSC without emitting files, just for checking
        # Pretty=false for easier Regex parsing
        result = subprocess.run(
            ["npx", "tsc", "--noEmit", "--pretty", "false"],
            cwd=self.root,
            capture_output=True,
            text=True,
            shell=True
        )
        return result.stdout

    def parse_errors(self, raw_output):
        # Regex to capture TSC error pattern: 
        # path/to/file.tsx(line,col): error TSXXXX: message
        pattern = r"(.+)\((\d+),(\d+)\): error (TS\d+): (.+)"
        matches = re.findall(pattern, raw_output)
        
        for file_path, line, col, code, msg in matches:
            clean_path = file_path.strip()
            full_path = self.root / clean_path
            
            if full_path.exists():
                self.report["total_errors"] += 1
                if clean_path not in self.report["files_affected"]:
                    self.report["files_affected"].append(clean_path)
                    
                    # Organize original file in /erros folder for audit
                    dest_error = self.folders["erros"] / clean_path
                    dest_error.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(full_path, dest_error)

                self.report["details"].append({
                    "file": clean_path,
                    "line": int(line),
                    "column": int(col),
                    "type": "TypeScript Typing",
                    "code": code,
                    "message": msg.strip()
                })

    def generate_summary(self):
        log_path = self.folders["logs"] / "diagnostic_report.json"
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        
        print("\nAudit Completed!")
        print(f"Total Errors: {self.report['total_errors']}")
        print(f"Affected Files: {len(self.report['files_affected'])}")
        print(f"Report generated at: {log_path}")

    def execute(self):
        if not self.root.exists():
            print(f"Error: Folder '{self.root}' not found at root.")
            return
        self.setup()
        raw_output = self.run_tsc_audit()
        self.parse_errors(raw_output)
        self.generate_summary()

if __name__ == "__main__":
    auditor = FrontendAuditor()
    auditor.execute()

