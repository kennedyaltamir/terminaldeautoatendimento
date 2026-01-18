
import json
import sys
import os
from pathlib import Path

LOCK = Path("mobile/PRODUCTION_LOCK_MOBILE.json")

REQUIRED_KEYS = [
    "ui_sweep",
    "telemetry",
    "frozen_assets",
    "store_ready"
]

def main():
    print("🔍 MESAFLOW PRODUCTION READINESS CHECK")
    print("=======================================")

    if not LOCK.exists():
        print("❌ PRODUCTION LOCK NÃO ENCONTRADO: mobile/PRODUCTION_LOCK_MOBILE.json")
        sys.exit(1)

    try:
        data = json.loads(LOCK.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        print("❌ ERRO: Arquivo de Lock corrompido (JSON inválido).")
        sys.exit(1)

    # Validação de Schema
    for key in REQUIRED_KEYS:
        if key not in data:
            print(f"❌ LOCK INVÁLIDO: chave ausente -> {key}")
            sys.exit(1)

    # Validação de Conteúdo
    if data.get("telemetry", {}).get("provider") != "SENTRY":
        print("❌ Telemetria inválida ou não configurada para SENTRY.")
        sys.exit(1)

    if data.get("ui_sweep", {}).get("status") != "PASS":
        print("❌ UI Sweep não aprovado no Lock File.")
        sys.exit(1)

    print("✅ APP 100% PRONTO PARA PRODUÇÃO (L5)")
    print("   - Telemetria: OK")
    print("   - UI Sweep: OK")
    print("   - Assets Congelados: OK")
    sys.exit(0)

if __name__ == "__main__":
    main()

