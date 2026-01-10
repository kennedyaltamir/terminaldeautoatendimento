import os
import sys

# [TEST_EXEMPT: Script utilitário de verificação de integridade local]

def check_files():
    """
    Valida a existência dos arquivos criados/modificados nesta sessão.
    """
    # Lista de arquivos críticos gerados nesta conversa
    session_files = [
        # Governança e Prompts
        "docs/Prompts/System_Instructions.xml",
        "docs/Prompts/Master_Handover.xml",
        "docs/architecture/domain-separation.md",
        "docs/MASTER_CONTEXT.md",
        
        # Backend (Fiscal & Features)
        "app/schemas.py",
        "app/routers/admin_features.py",
        "app/services/feature_flag_service.py",
        "app/services/fiscal/factory.py",
        "app/services/fiscal/providers/focus_nfe.py",
        
        # Frontend Web
        "frontend/src/lib/jwt.ts",
        "frontend/src/lib/featureFlagsApi.ts",
        "frontend/src/context/FeatureFlagContext.tsx",
        "frontend/src/components/admin/FeatureToggleCard.tsx",
        "frontend/src/app/admin/[slug]/settings/features/page.tsx",
        
        # Mobile (Infra & App Layer)
        "mobile/package.json",
        "mobile/app.json",
        "mobile/tsconfig.json",
        "mobile/App.tsx",
        "mobile/src/config/env.ts",
        "mobile/src/types/auth.ts",
        "mobile/src/types/auth.types.ts",
        "mobile/src/services/auth/storage.ts",
        "mobile/src/services/auth/client.ts",
        "mobile/src/services/api.ts",
        "mobile/src/store/auth.store.ts",
        
        # Documentação Mobile
        "docs/mobile/README.md",
        "docs/mobile/architecture/MOBILE_ARCHITECTURE.md",
        "docs/mobile/architecture/INTEGRATION_STRATEGY.md",
        "docs/mobile/architecture/APP_ARCHITECTURE.md",
        "docs/mobile/decisions/MISSION_GOVERNANCE.md",
        "docs/mobile/decisions/FUNCTIONAL_MAPPING.md",
        "docs/mobile/decisions/DATA_STRATEGY.md",
        "docs/mobile/tasks/mobile_11_auth_infra.md",
        "docs/mobile/tasks/mobile_12_auth_application.md",
        
        # Scripts de Teste e Validação
        "scripts/setup/verify_mobile_setup.py",
        "scripts/setup/verify_mobile_auth.py",
        "scripts/setup/verify_mobile_state.py",
        "scripts/tests/test_feature_flags_contract.py",
        "scripts/tests/test_fiscal_sandbox.py",
        "scripts/tests/test_fiscal_production_safeguard.py",
        
        # Relatórios
        "docs/reports/FISCAL_PRODUCTION_GO_LIVE.md",
        "docs/specs/FISCAL_HOMOLOGATION.md",
        "docs/specs/FISCAL_PRODUCTION_CHECKLIST.md",
        "docs/specs/FEATURE_FLAGS_UI.md"
    ]

    print(f"🔍 Iniciando verificação de {len(session_files)} arquivos da sessão...\n")
    
    missing = []
    found = 0

    for file_path in session_files:
        if os.path.exists(file_path):
            print(f"✅ [OK] {file_path}")
            found += 1
        else:
            print(f"❌ [FALTANDO] {file_path}")
            missing.append(file_path)

    print("\n" + "="*50)
    print(f"📊 RESUMO: {found} encontrados, {len(missing)} ausentes.")
    
    if missing:
        print("\n🚨 ATENÇÃO: Os arquivos listados como FALTANDO não foram detectados.")
        print("Certifique-se de ter rodado o 'python atualizar.py' com as respostas da IA.")
        sys.exit(1)
    else:
        print("\n✨ INTEGRIDADE CONFIRMADA: Todos os arquivos da sessão estão presentes.")
        sys.exit(0)

if __name__ == "__main__":
    check_files()
