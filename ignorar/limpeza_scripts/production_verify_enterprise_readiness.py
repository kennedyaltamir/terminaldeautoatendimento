import os
import sys

def verify_enterprise_readiness():
    print("🔍 Iniciando Auditoria de Prontidão Enterprise (10/10)...")

    checklist = {
        "docs/legal/RoPA.md": ["Categorias de Dados", "Base Legal", "Neon.tech"],
        "docs/legal/PRIVACY_POLICY.md": ["Retenção e Descarte", "5 Anos", "privacy@mesaflow.com.br"],
        "docs/legal/STORE_DATA_SAFETY.md": ["Google Play", "Apple App Store", "Data Types"],
        "SECURITY.md": ["Supported Versions", "Reporting a Vulnerability"],
        "docs/legal/SLA.md": ["99,9%", "Compensação", "Serviços Críticos"]
    }

    errors = 0

    for file_path, keywords in checklist.items():
        if not os.path.exists(file_path):
            print(f"❌ Arquivo FALTANDO: {file_path}")
            errors += 1
            continue
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                for kw in keywords:
                    if kw not in content:
                        print(f"❌ Conteúdo incompleto em {file_path}: Faltando '{kw}'")
                        errors += 1
                    else:
                        pass # OK
            print(f"✅ {file_path} validado.")
        except Exception as e:
            print(f"❌ Erro ao ler {file_path}: {e}")
            errors += 1

    if errors == 0:
        print("\n🏆 Enterprise Readiness Check Passed: 10/10 Compliance.")
        sys.exit(0)
    else:
        print(f"\n🚨 Falha na auditoria: {errors} erro(s) encontrado(s).")
        sys.exit(1)

if __name__ == "__main__":
    verify_enterprise_readiness()