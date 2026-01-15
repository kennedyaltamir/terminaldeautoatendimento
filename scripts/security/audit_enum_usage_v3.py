
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 11:05:00
import ast
import os
import sys
from pathlib import Path

# Configuração
MODELS_DIR = Path("app/models")
SERVICES_DIR = Path("app/services")
SENSITIVE_FIELDS = {"status", "role", "tier", "type", "provider", "segment", "station"}

def audit_models():
    print("🔍 Auditando Models por uso proibido de Enum()...")
    errors = []
    
    for path in MODELS_DIR.rglob("*.py"):
        try:
            content = path.read_text(encoding="utf-8")
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
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

    return errors

def audit_services():
    print("🔍 Auditando Services por atribuições inseguras...")
    errors = []
    
    for path in SERVICES_DIR.rglob("*.py"):
        try:
            content = path.read_text(encoding="utf-8")
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                # Procura por atribuições: obj.field = value
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Attribute) and target.attr in SENSITIVE_FIELDS:
                            # Verifica se o valor atribuído é uma chamada a normalize_enum
                            is_safe = False
                            if isinstance(node.value, ast.Call):
                                if isinstance(node.value.func, ast.Name) and node.value.func.id == "normalize_enum":
                                    is_safe = True
                            
                            # Exceção: Atribuição de literais hardcoded (ex: status = "pending") é aceitável se for lowercase
                            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                                if node.value.value == node.value.value.lower():
                                    is_safe = True

                            if not is_safe:
                                errors.append(f"❌ {path.name}:{node.lineno} - Atribuição insegura em '{target.attr}'. Use normalize_enum().")
                
                # Procura por AugAssign (+=)
                if isinstance(node, ast.AugAssign):
                    if isinstance(node.target, ast.Attribute) and node.target.attr in SENSITIVE_FIELDS:
                        errors.append(f"❌ {path.name}:{node.lineno} - AugAssign inseguro em '{node.target.attr}'.")

                # Procura por setattr
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "setattr":
                    if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and node.args[1].value in SENSITIVE_FIELDS:
                        errors.append(f"❌ {path.name}:{node.lineno} - setattr inseguro em '{node.args[1].value}'.")

        except Exception as e:
            print(f"⚠️ Erro ao ler {path}: {e}")

    return errors

if __name__ == "__main__":
    model_errors = audit_models()
    service_errors = audit_services()
    
    all_errors = model_errors + service_errors
    
    if all_errors:
        print("\n🚨 VIOLAÇÕES ENCONTRADAS (RFC-009 v1.3):")
        for e in all_errors:
            print(e)
        sys.exit(1)
    
    print("\n✅ Auditoria de Enums: APROVADA (Models & Services).")
    sys.exit(0)

