
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 09:10:00
import ast
import os
import sys
from pathlib import Path

# Configuração
MODELS_DIR = Path("app/models")
SENSITIVE_FIELDS = {"status", "role", "tier", "type", "provider", "segment"}

def audit_models():
    print("🔍 Auditando Models por uso proibido de Enum()...")
    errors = []
    
    for path in MODELS_DIR.rglob("*.py"):
        try:
            content = path.read_text(encoding="utf-8")
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                # Procura por Column(Enum(...)) ou Column(SQLEnum(...))
                if isinstance(node, ast.Call) and hasattr(node.func, "id") and node.func.id == "Column":
                    for arg in node.args:
                        if isinstance(arg, ast.Call):
                            func_name = ""
                            if isinstance(arg.func, ast.Name):
                                func_name = arg.func.id
                            elif isinstance(arg.func, ast.Attribute):
                                func_name = arg.func.attr
                            
                            if func_name in ["Enum", "SQLEnum"]:
                                errors.append(f"❌ {path.name}:{node.lineno} - Uso de SQLAlchemy Enum detectado!")
        except Exception as e:
            print(f"⚠️ Erro ao ler {path}: {e}")

    if errors:
        print("\n🚨 VIOLAÇÕES ENCONTRADAS (RFC-009):")
        for e in errors:
            print(e)
        return False
    
    print("✅ Nenhum uso de Enum() detectado nos Models.")
    return True

if __name__ == "__main__":
    if not audit_models():
        sys.exit(1)
    sys.exit(0)

