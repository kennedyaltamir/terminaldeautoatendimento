import sys
import os

def verify():
    print("🔍 Verificando TASK-023: Modo Silencioso e Alertas...")
    
    # 1. Verificação de Existência de Arquivos
    required_files = [
        "mobile/src/store/settings.store.ts",
        "mobile/src/services/alerts/alerts.output.service.ts",
        "mobile/src/screens/orders/OrdersScreen.tsx"
    ]
    
    for f_path in required_files:
        if not os.path.exists(f_path):
            print(f"❌ Arquivo faltando: {f_path}")
            sys.exit(1)
        print(f"✅ Arquivo encontrado: {f_path}")

    # 2. Verificação de Conteúdo (Lógica Implementada)
    
    # Settings Store
    with open("mobile/src/store/settings.store.ts", "r", encoding="utf-8") as f:
        content = f.read()
        if "isSilentMode" not in content:
            print("❌ 'isSilentMode' não encontrado na SettingsStore.")
            sys.exit(1)
        if "persist" not in content:
            print("❌ Persistência não configurada na SettingsStore.")
            sys.exit(1)

    # Alerts Output Service
    with open("mobile/src/services/alerts/alerts.output.service.ts", "r", encoding="utf-8") as f:
        content = f.read()
        if "useSettingsStore.getState().isSilentMode" not in content:
            print("❌ AlertsOutputService não está consultando o Modo Silencioso.")
            sys.exit(1)
        if "Vibration.vibrate" not in content:
            print("❌ Chamada de vibração não encontrada.")
            sys.exit(1)

    # Orders Screen (UI)
    with open("mobile/src/screens/orders/OrdersScreen.tsx", "r", encoding="utf-8") as f:
        content = f.read()
        if "toggleSilentMode" not in content:
            print("❌ Ação de toggle não conectada na UI.")
            sys.exit(1)
        if "Bell" not in content or "BellOff" not in content:
            print("❌ Ícones de sino (Bell/BellOff) não encontrados na UI.")
            sys.exit(1)

    print("\n🏆 TASK-023: VALIDAÇÃO ESTRUTURAL CONCLUÍDA COM SUCESSO.")
    print("   (Nota: Teste funcional de vibração requer dispositivo físico/emulador)")
    sys.exit(0)

if __name__ == "__main__":
    verify()
