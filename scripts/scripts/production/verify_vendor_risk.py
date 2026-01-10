import os
import sys

def verify_vendor_risk():
    print("🔍 Iniciando Verificação de Gestão de Risco de Fornecedores (TASK-ENT-04)...")

    # 1. Verificar Existência dos Arquivos
    files = [
        "docs/enterprise/VENDOR_RISK_ASSESSMENT.md",
        "docs/legal/SUBPROCESSORS.md"
    ]

    for f in files:
        if not os.path.exists(f):
            print(f"❌ Arquivo FALTANDO: {f}")
            sys.exit(1)
        print(f"✅ Arquivo encontrado: {f}")

    # 2. Verificar Fornecedores Críticos (Tier 1)
    # Estes devem constar obrigatoriamente em ambos os documentos
    critical_vendors = [
        "Neon",
        "Render",
        "Stripe",
        "Mercado Pago"
    ]

    # Verificar VENDOR_RISK_ASSESSMENT.md
    with open("docs/enterprise/VENDOR_RISK_ASSESSMENT.md", "r", encoding="utf-8") as f:
        content = f.read()
        for vendor in critical_vendors:
            if vendor not in content:
                print(f"❌ Fornecedor crítico '{vendor}' ausente no Risk Assessment.")
                sys.exit(1)
        
        # Verificar se há menção a SOC2 ou ISO
        if "SOC 2" not in content and "ISO 27001" not in content:
            print("❌ Nenhuma certificação de segurança (SOC2/ISO) citada no Risk Assessment.")
            sys.exit(1)

    # Verificar SUBPROCESSORS.md
    with open("docs/legal/SUBPROCESSORS.md", "r", encoding="utf-8") as f:
        content = f.read()
        for vendor in critical_vendors:
            # Ajuste para nomes legais (ex: MercadoLibre para Mercado Pago)
            search_term = "MercadoLibre" if vendor == "Mercado Pago" else vendor
            if search_term not in content:
                print(f"❌ Fornecedor crítico '{search_term}' ausente na lista pública de Sub-processadores.")
                sys.exit(1)

    print("\n🏆 Vendor Risk Assessment Verified: All critical vendors mapped.")
    sys.exit(0)

if __name__ == "__main__":
    verify_vendor_risk()
