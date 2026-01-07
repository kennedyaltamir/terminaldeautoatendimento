import os
import sys

# [TEST_EXEMPT: Script de auditoria de integridade para Handover]

def verify():
    print("🔍 Iniciando Auditoria Final para Handover (v5.4)...")

    # Arquivos críticos criados/estabilizados nesta jornada mobile
    critical_files = [
        # Infra & Auth
        "mobile/src/services/api.ts",
        "mobile/src/services/auth/jwt.ts",
        "mobile/src/store/auth.store.ts",
        "mobile/src/store/session.store.ts",
        "mobile/src/services/session.bootstrap.service.ts",
        
        # Design System (UI Foundation)
        "mobile/src/ui/tokens/colors.ts",
        "mobile/src/ui/tokens/spacing.ts",
        "mobile/src/ui/tokens/typography.ts",
        "mobile/src/ui/components/Button.tsx",
        "mobile/src/ui/components/Input.tsx",
        "mobile/src/ui/components/Card.tsx",
        
        # Realtime & Business
        "mobile/src/types/realtime.events.ts",
        "mobile/src/services/orders.realtime.service.ts",
        "mobile/src/services/orders.sync.service.ts",
        "mobile/src/services/realtime.reconnect.policy.ts",
        "mobile/src/services/alerts/alerts.engine.service.ts",
        "mobile/src/store/orders.store.ts",
        "mobile/src/screens/orders/OrdersScreen.tsx",
        
        # Documentation
        "docs/TECH_DEBT.md",
        "docs/TASKS.md",
        "docs/mobile/decisions/JWT_BACKEND_AUDIT.md",
        "docs/Prompts/System_Instructions.xml"
    ]

    missing = []
    for f in critical_files:
        if os.path.exists(f):
            print(f"✅ {f}")
        else:
            print(f"❌ FALTANDO: {f}")
            missing.append(f)

    print("\n" + "="*50)
    
    # Verificação de Lixo na Raiz
    trash_detected = []
    possible_trash = ["state.status)", "state.slug)", "{", "path", "atualizar.log"]
    for t in possible_trash:
        if os.path.exists(t):
            trash_detected.append(t)
    
    if trash_detected:
        print(f"⚠️  LIXO DETECTADO NA RAIZ: {trash_detected}")
        print("💡 Sugestão: Delete estes arquivos para um contexto mais limpo.")

    if not missing:
        print("\n✨ TUDO SINCRONIZADO. Você está pronto para gerar o 'todososarquivos.txt'.")
        sys.exit(0)
    else:
        print(f"\n🚨 ALERTA: {len(missing)} arquivos críticos não encontrados.")
        sys.exit(1)

if __name__ == "__main__":
    verify()
