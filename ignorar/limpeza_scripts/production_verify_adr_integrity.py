
import os
import sys
import re

def verify_adr_integrity():
    print("🔍 Iniciando Verificação de Integridade de ADRs (TASK-ENT-05)...")

    adr_dir = "docs/adr"
    
    # 1. Verificar Diretório
    if not os.path.exists(adr_dir):
        print(f"❌ Diretório {adr_dir} não encontrado.")
        sys.exit(1)

    # 2. Listar Arquivos Esperados
    expected_files = [
        "ADR-000_INDEX.md",
        "ADR-001_FASTAPI_BACKEND.md",
        "ADR-002_NEON_POSTGRESQL.md",
        "ADR-003_RENDER_RUNTIME.md",
        "ADR-004_DUAL_HEALTH_ENDPOINT.md",
        "ADR-005_SECURITY_HARDENING_STRATEGY.md"
    ]

    files_found = os.listdir(adr_dir)
    
    for f in expected_files:
        if f not in files_found:
            print(f"❌ Arquivo ADR faltando: {f}")
            sys.exit(1)
        print(f"✅ Encontrado: {f}")

    # 3. Validar Estrutura Interna
    required_sections = ["Contexto", "Decisão", "Alternativas Consideradas", "Consequências"]
    
    for f in expected_files:
        path = os.path.join(adr_dir, f)
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
            
            # Ignora validação de seções para o INDEX, pois ele tem formato diferente
            if "INDEX" in f:
                if "ADR-001" not in content:
                    print(f"❌ Index não referencia ADR-001.")
                    sys.exit(1)
                continue

            for section in required_sections:
                if section not in content:
                    print(f"❌ Seção '{section}' ausente em {f}")
                    sys.exit(1)
            
            # Valida Status com Regex para suportar formatação Markdown (**Status:** ou Status:)
            # Aceita: ACEITA, DEPRECIADA, SUPERSEDED
            status_pattern = r"\**Status:?\**\s*(ACEITA|DEPRECIADA|SUPERSEDED)"
            
            if not re.search(status_pattern, content, re.IGNORECASE):
                 print(f"❌ Status inválido ou ausente em {f}")
                 sys.exit(1)

    print("\n🏆 ADR Master Log Verified: All architectural decisions are documented and consistent.")
    sys.exit(0)

if __name__ == "__main__":
    verify_adr_integrity()