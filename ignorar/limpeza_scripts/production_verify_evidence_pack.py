import os
import sys

def verify_evidence_pack():
    print("🔍 Iniciando Verificação do Enterprise Evidence Pack (TASK-ENT-02)...")

    target_file = "docs/enterprise/EVIDENCE_PACK.md"

    # 1. Verificação de Existência
    if not os.path.exists(target_file):
        print(f"❌ Arquivo FALTANDO: {target_file}")
        sys.exit(1)
    
    print(f"✅ Arquivo encontrado: {target_file}")

    # 2. Verificação de Conteúdo Crítico (Keywords)
    required_keywords = [
        "Row-Level Security",
        "RLS",
        "HSTS",
        "CSP",
        "LGPD",
        "SLA",
        "Sentry",
        "Neon.tech",
        "Pentest",
        "security@mesaflow.com.br"
    ]

    try:
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
            
            missing = []
            for kw in required_keywords:
                if kw not in content:
                    missing.append(kw)
            
            if missing:
                print(f"❌ Conteúdo incompleto. Palavras-chave ausentes: {missing}")
                sys.exit(1)
            
            print("✅ Conteúdo validado: Todas as seções críticas presentes.")

    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        sys.exit(1)

    print("\n🏆 Evidence Pack Verified: Ready for Due Diligence.")
    sys.exit(0)

if __name__ == "__main__":
    verify_evidence_pack()