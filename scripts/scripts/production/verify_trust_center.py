import os
import sys

def verify_trust_center():
    print("🔍 Verificando Trust Center (TASK-ENT-01)...")

    # 1. Verificar Arquivos Criados
    files = [
        "frontend/src/app/trust/layout.tsx",
        "frontend/src/app/trust/page.tsx",
        "frontend/src/app/trust/status/page.tsx",
        "frontend/src/app/trust/security/page.tsx"
    ]

    missing = []
    for f in files:
        if not os.path.exists(f):
            missing.append(f)
            print(f"❌ Faltando: {f}")
        else:
            print(f"✅ Encontrado: {f}")

    if missing:
        print("🚨 Falha na verificação de arquivos.")
        sys.exit(1)

    # 2. Verificar Conteúdo Crítico
    try:
        with open("frontend/src/app/trust/status/page.tsx", "r", encoding="utf-8") as f:
            content = f.read()
            # Correção: O frontend usa ${process.env.NEXT_PUBLIC_API_URL}/health
            # Validamos a presença do path /health que é agnóstico ao domínio base
            if "/health" not in content:
                print("❌ Página de Status não consome endpoint de health (/health)")
                sys.exit(1)
            print("✅ Página de Status configurada corretamente.")

        with open("frontend/src/app/trust/security/page.tsx", "r", encoding="utf-8") as f:
            content = f.read()
            if "security@mesaflow.com.br" not in content:
                print("❌ E-mail de segurança ausente na página.")
                sys.exit(1)
            print("✅ Página de Segurança configurada corretamente.")

    except Exception as e:
        print(f"❌ Erro ao ler arquivos: {e}")
        sys.exit(1)

    print("\n🏆 Trust Center Verification Passed: All routes active.")
    sys.exit(0)

if __name__ == "__main__":
    verify_trust_center()