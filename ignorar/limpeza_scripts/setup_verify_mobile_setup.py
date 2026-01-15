import os
import sys
from pathlib import Path

# [TEST_EXEMPT: Script de validação estrutural de infraestrutura, sem lógica de negócio testável. A verificação é realizada por execução direta do script.]

# ==============================================================================
# CONFIGURAÇÃO DE VALIDAÇÃO (v1.3)
# ==============================================================================

# Lista de arquivos e diretórios que DEVEM existir para o ambiente mobile.
# Adicionados assets técnicos obrigatórios para o Expo.
CRITICAL_PATHS = [
    "mobile/package.json",
    "mobile/app.json",
    "mobile/tsconfig.json",
    "mobile/App.tsx",
    "mobile/babel.config.js",
    "mobile/assets/icon.png",
    "mobile/assets/splash.png",
    "mobile/assets/adaptive-icon.png",
    "mobile/assets/favicon.png",
]

# Mapeamento de arquivos e strings que DEVEM estar contidas neles.
CONTENT_VALIDATIONS = {
    ".gitignore": [
        "mobile/node_modules/",
        "mobile/.expo/",
        "mobile/dist/",
    ]
}

def validate_environment():
    """
    Executa a validação estrutural do ambiente mobile.
    Garante compatibilidade com Unicode no Windows através de encoding="utf-8".
    """
    print("🔍 Starting environment validation (v1.3)...")
    
    errors_found = 0
    
    # 1. Validação de Existência de Caminhos
    print("\n--- Checking critical paths ---")
    for path_str in CRITICAL_PATHS:
        path = Path(path_str)
        if path.exists():
            print(f"✅ Found: {path_str}")
        else:
            print(f"❌ Missing: {path_str}")
            errors_found += 1

    # 2. Validação de Conteúdo de Arquivos
    print("\n--- Validating file contents ---")
    for file_path_str, required_strings in CONTENT_VALIDATIONS.items():
        file_path = Path(file_path_str)
        
        if not file_path.exists():
            print(f"❌ File not found for content validation: {file_path_str}")
            errors_found += 1
            continue
            
        try:
            with open(file_path, mode="r", encoding="utf-8") as f:
                content = f.read()
                
            for s in required_strings:
                if s in content:
                    print(f"✅ '{s}' found in {file_path_str}")
                else:
                    print(f"❌ '{s}' NOT found in {file_path_str}")
                    errors_found += 1
                    
        except Exception as e:
            print(f"❌ Error reading {file_path_str}: {str(e)}")
            errors_found += 1

    # --- RESULTADO FINAL ---
    print("\n" + "="*40)
    if errors_found == 0:
        print("✨ Environment validation completed successfully.")
        sys.exit(0)
    else:
        print(f"🚨 Validation failed with {errors_found} error(s).")
        sys.exit(1)

if __name__ == "__main__":
    try:
        validate_environment()
    except KeyboardInterrupt:
        print("\n\nValidation aborted by user.")
        sys.exit(1)
