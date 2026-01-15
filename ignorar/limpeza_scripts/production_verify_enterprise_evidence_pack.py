import os
import sys

def verify_evidence_pack():
    print("🔍 Iniciando Verificação do Enterprise Evidence Pack (TASK-ENT-02)...")

    base_path = "docs/enterprise/evidence_pack"
    
    # 1. Verificar Diretório
    if not os.path.exists(base_path):
        print(f"❌ Diretório base não encontrado: {base_path}")
        sys.exit(1)

    # 2. Lista de Arquivos Obrigatórios
    required_files = [
        "ENTERPRISE_EVIDENCE_INDEX.md",
        "SECURITY_OVERVIEW.md",
        "ARCHITECTURE_OVERVIEW.md",
        "DATA_PROTECTION_AND_LGPD.md",
        "AVAILABILITY_AND_SLA.md",
        "INCIDENT_RESPONSE.md",
        "VENDOR_AND_SUBPROCESSORS.md"
    ]

    missing_files = []
    for f in required_files:
        path = os.path.join(base_path, f)
        if not os.path.exists(path):
            print(f"❌ Arquivo FALTANDO: {f}")
            missing_files.append(f)
        else:
            print(f"✅ Arquivo encontrado: {f}")

    if missing_files:
        print("🚨 Falha na verificação de arquivos.")
        sys.exit(1)

    # 3. Validação de Conteúdo Cruzado (Integridade)
    # Verifica se o Index referencia todos os arquivos
    index_path = os.path.join(base_path, "ENTERPRISE_EVIDENCE_INDEX.md")
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
            for rf in required_files:
                if rf == "ENTERPRISE_EVIDENCE_INDEX.md": continue
                if rf not in content:
                    print(f"❌ O Índice não referencia o arquivo: {rf}")
                    sys.exit(1)
            print("✅ Índice mestre validado (Links cruzados OK).")
    except Exception as e:
        print(f"❌ Erro ao ler índice: {e}")
        sys.exit(1)

    print("\n🏆 Enterprise Evidence Pack Verified: Ready for Sales, Audit and Due Diligence.")
    sys.exit(0)

if __name__ == "__main__":
    verify_evidence_pack()
