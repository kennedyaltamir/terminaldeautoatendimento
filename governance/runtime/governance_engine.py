import re
import json
import sys
import os
from pathlib import Path

class GovernanceEngine:
    def __init__(self):
        self.contract_path = Path("governance/runtime/role_contracts.json")
        self.contract = json.loads(self.contract_path.read_text(encoding="utf-8")) if self.contract_path.exists() else {}
        self.violations = []

    def _normalize_path(self, p: str) -> str:
        """Normaliza caminhos para evitar bypass via path traversal ou aliases."""
        return os.path.normpath(p).replace("\\", "/").lower().strip("/")

    def validate_output(self, content: str):
        if not self.contract:
            return True

        lines = [l for l in content.splitlines() if l.strip()]
        
        if not lines or not re.match(self.contract["global_requirements"]["mandatory_header"], lines[0]):
            self.violations.append("CRITICAL_VIOLATION: ROLE header must be the first non-empty line.")
            return False

        role = re.search(r"ROLE=(\w+)", lines[0]).group(1)
        role_rules = self.contract["roles"].get(role, {})

        for p in self.contract["global_requirements"]["forbidden_global"]:
            if p.lower() in content.lower():
                self.violations.append(f"GLOBAL_FORBIDDEN: Found unauthorized pattern '{p}'")

        for pattern in role_rules.get("forbidden_patterns", []):
            if re.search(pattern, content, re.I):
                self.violations.append(f"ROLE_VIOLATION ({role}): Forbidden pattern detected: '{pattern}'")

        if role == "EXECUTOR":
            if role_rules.get("strict_block_enforcement"):
                in_block = False
                for line in lines[1:]:
                    clean_line = line.strip()
                    if clean_line.startswith("[[MESAFLOW_BEGIN:"):
                        in_block = True
                        continue
                    if clean_line.startswith("[[MESAFLOW_END]]"):
                        in_block = False
                        continue
                    
                    if not in_block and clean_line:
                        self.violations.append(f"FORMAT_VIOLATION: Executor cannot output text outside blocks: '{clean_line[:30]}...'")

            if role_rules.get("critical_files_protection"):
                protected = [self._normalize_path(f) for f in self.contract.get("protected_files", [])]
                requested_files = re.findall(r"\[\[MESAFLOW_BEGIN:(.*?)\]\]", content)
                for f in requested_files:
                    if self._normalize_path(f) in protected:
                        self.violations.append(f"SECURITY_VIOLATION: Unauthorized attempt to modify kernel file: {f}")

        return len(self.violations) == 0

    def report(self):
        if self.violations:
            print("❌ GOVERNANCE ENGINE: FAIL")
            for v in self.violations:
                print(f"   - {v}")
            return False
        print("✅ GOVERNANCE ENGINE: PASS")
        return True

if __name__ == "__main__":
    target = Path("resposta.txt")
    if not target.exists():
        sys.exit(0)
    
    engine = GovernanceEngine()
    if not engine.validate_output(target.read_text(encoding="utf-8")):
        engine.report()
        sys.exit(1)
    sys.exit(0)