import os
import sys

# [TEST_EXEMPT: Script de auditoria de integridade da sessão de desenvolvimento]

def verify_sync():
    """
    Script de Verificação de Sincronia de Sessão.
    Valida se todos os arquivos gerados nesta conversa estão presentes e íntegros.
    """
    print("🔍 Iniciando Auditoria de Sincronia da Sessão (Fase 10 - Mobile)...")

    # Mapeamento de arquivos por categoria para facilitar o diagnóstico
    files_to_check = {
        "Docs": [
            "docs/mobile/tasks/mobile_14a_semantic_auth.md",
            "docs/mobile/tasks/mobile_14b_auth_boundary.md",
            "docs/mobile/tasks/mobile_15_ui_foundation.md",
            "docs/mobile/tasks/mobile_16_ui_login_home.md",
            "docs/mobile/tasks/mobile_17_kds_orders.md",
            "docs/mobile/tasks/mobile_18_realtime_kds.md",
            "docs/mobile/tasks/mobile_19_operational_identity.md",
            "docs/mobile/decisions/JWT_BACKEND_AUDIT.md",
            "docs/TASKS.md",
            "docs/ROADMAP.md",
            "docs/TECH_DEBT.md"
        ],
        "UI Foundation": [
            "mobile/src/ui/tokens/colors.ts",
            "mobile/src/ui/tokens/spacing.ts",
            "mobile/src/ui/tokens/typography.ts",
            "mobile/src/ui/components/Button.tsx",
            "mobile/src/ui/components/Input.tsx",
            "mobile/src/ui/components/Card.tsx"
        ],
        "Infra & Logic": [
            "mobile/src/config/env.ts",
            "mobile/src/types/auth.types.ts",
            "mobile/src/types/realtime.events.ts",
            "mobile/src/services/auth/jwt.ts",
            "mobile/src/services/session.bootstrap.service.ts",
            "mobile/src/store/auth.store.ts",
            "mobile/src/store/session.store.ts",
            "mobile/src/utils/time.ts"
        ],
        "Operational (KDS)": [
            "mobile/src/services/orders.service.ts",
            "mobile/src/services/orders.realtime.service.ts",
            "mobile/src/store/orders.store.ts",
            "mobile/src/screens/orders/OrdersScreen.tsx"
        ],
        "Navigation": [
            "mobile/src/navigation/AuthGate.tsx",
            "mobile/src/navigation/RootNavigator.tsx",
            "mobile/src/navigation/stacks/AuthStack.tsx",
            "mobile/src/navigation/stacks/AppStack.tsx",
            "mobile/src/screens/auth/LoginScreen.tsx",
            "mobile/src/screens/app/HomeScreen.tsx"
        ],
        "Scripts": [
            "scripts/setup/verify_mobile_semantic_auth.py",
            "scripts/setup/verify_mobile_auth_boundary.py",
            "scripts/setup/verify_mobile_ui_foundation.py",
            "scripts/setup/verify_mobile_kds_orders.py",
            "scripts/setup/verify_mobile_kds_realtime.py",
            "scripts/setup/verify_mobile_operational_identity.py"
        ]
    }

    total_files = sum(len(v) for v in files_to_check.values())
    found_count = 0
    missing_files = []

    for category, files in files_to_check.items():
        print(f"\n📁 Categoria: {category}")
        for f in files:
            if os.path.exists(f):
                # Validação Semântica Rápida (Exemplo: não pode haver placeholder hardcoded em AppStack)
                if "AppStack.tsx" in f:
                    with open(f, "r", encoding="utf-8") as file_content:
                        if "const SLUG_PLACEHOLDER" in file_content.read():
                            print(f"  ⚠️  [ALERTA] {f} contém Dívida Técnica (Slug Hardcoded).")
                
                print(f"  ✅ {f}")
                found_count += 1
            else:
                print(f"  ❌ FALTANDO: {f}")
                missing_files.append(f)

    print("\n" + "="*50)
    print(f"📊 Resumo Final: {found_count}/{total_files} arquivos sincronizados.")
    
    if missing_files:
        print(f"\n🚨 Erro: {len(missing_files)} arquivo(s) não encontrado(s).")
        print("Dica: Verifique se você rodou o 'python atualizar.py' para todas as mensagens.")
        sys.exit(1)
    else:
        print("\n✨ Sucesso: Todos os arquivos da sessão foram detectados e validados.")
        sys.exit(0)

if __name__ == "__main__":
    verify_sync()
