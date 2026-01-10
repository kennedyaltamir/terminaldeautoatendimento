import os
import sys

def verify_security_disclosure():
    print("🔍 Iniciando Verificação de Prontidão Legal de Segurança (TASK-ENT-06)...")

    # 1. Verificar Arquivos
    files = [
        "docs/legal/SECURITY_DISCLOSURE.md",
        "docs/legal/DATA_BREACH_NOTIFICATION.md",
        "SECURITY.md"
    ]

    missing = []
    for f in files:
        if not os.path.exists(f):
            print(f"❌ Arquivo FALTANDO: {f}")
            missing.append(f)
        else:
            print(f"✅ Arquivo encontrado: {f}")

    if missing:
        print("🚨 Falha na verificação de arquivos.")
        sys.exit(1)

    # 2. Verificar Conteúdo Crítico
    checks = {
        "docs/legal/SECURITY_DISCLOSURE.md": ["Safe Harbor", "security@mesaflow.com.br", "In-Scope"],
        "docs/legal/DATA_BREACH_NOTIFICATION.md": ["48 horas", "ANPD", "Controlador", "Operador"],
        "SECURITY.md": ["Responsible Disclosure Policy", "Data Breach Notification Policy"]
    }

    for file_path, keywords in checks.items():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                for kw in keywords:
                    if kw not in content:
                        print(f"❌ Palavra-chave '{kw}' ausente em {file_path}")
                        sys.exit(1)
            print(f"✅ Conteúdo validado em {file_path}")
        except Exception as e:
            print(f"❌ Erro ao ler {file_path}: {e}")
            sys.exit(1)

    print("\n🏆 Security Disclosure Readiness Verified: Policies are compliant.")
    sys.exit(0)

if __name__ == "__main__":
    verify_security_disclosure()
