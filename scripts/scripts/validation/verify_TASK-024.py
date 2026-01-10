import sys
import os

def verify():
    print("🔍 Verificando TASK-024: Resiliência de Rede...")
    
    # 1. Verificação de Existência de Arquivos
    required_files = [
        "mobile/src/services/realtime.reconnect.policy.ts",
        "mobile/src/services/orders.realtime.service.ts",
        "mobile/src/services/orders.sync.service.ts",
        "mobile/src/store/orders.store.ts"
    ]
    
    for f_path in required_files:
        if not os.path.exists(f_path):
            print(f"❌ Arquivo faltando: {f_path}")
            sys.exit(1)
        print(f"✅ Arquivo encontrado: {f_path}")

    # 2. Verificação de Conteúdo (Lógica Implementada)
    
    # Policy
    with open("mobile/src/services/realtime.reconnect.policy.ts", "r", encoding="utf-8") as f:
        content = f.read()
        if "MAX_RETRIES = 10" not in content:
            print("❌ Política de retries não definida corretamente.")
            sys.exit(1)
        if "Math.pow(2, this.retryCount)" not in content:
            print("❌ Lógica exponencial não encontrada.")
            sys.exit(1)

    # Realtime Service
    with open("mobile/src/services/orders.realtime.service.ts", "r", encoding="utf-8") as f:
        content = f.read()
        if "ReconnectPolicy.getNextDelay()" not in content:
            print("❌ Serviço não está usando a política de reconexão.")
            sys.exit(1)
        if "this._onReconnect()" not in content:
            print("❌ Callback de reconexão não implementado.")
            sys.exit(1)

    # Sync Service
    with open("mobile/src/services/orders.sync.service.ts", "r", encoding="utf-8") as f:
        content = f.read()
        if "performFullSync" not in content:
            print("❌ Método performFullSync não encontrado.")
            sys.exit(1)
        if "store.setSyncing(true)" not in content:
            print("❌ Flag de sincronização não está sendo ativada.")
            sys.exit(1)

    print("\n🏆 TASK-024: VALIDAÇÃO ESTRUTURAL CONCLUÍDA COM SUCESSO.")
    sys.exit(0)

if __name__ == "__main__":
    verify()
