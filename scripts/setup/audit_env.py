# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-09 23:58:00
import os
from pathlib import Path
from dotenv import dotenv_values

def audit():
    print("🔍 Iniciando Auditoria de Ambiente (MesaFlow OS)...")
    
    example_path = Path(".env.example")
    env_path = Path(".env")
    
    if not example_path.exists():
        print("❌ ERRO: .env.example não encontrado.")
        return

    # Carrega as chaves esperadas do exemplo
    expected_env = dotenv_values(example_path)
    # Carrega as chaves atuais do .env real
    current_env = dotenv_values(env_path) if env_path.exists() else {}

    missing = []
    placeholders = []
    
    print(f"\n{'VARIÁVEL':<30} | {'STATUS':<15}")
    print("-" * 50)

    for key in expected_env.keys():
        val = current_env.get(key)
        
        if not val:
            status = "❌ AUSENTE"
            missing.append(key)
        elif "YOUR_" in val or "SUA_" in val or val == "changeme":
            status = "⚠️  PLACEHOLDER"
            placeholders.append(key)
        else:
            status = "✅ OK"
        
        print(f"{key:<30} | {status}")

    print("-" * 50)
    
    if missing:
        print(f"\n🚨 CRÍTICO: {len(missing)} variáveis obrigatórias não encontradas no seu .env.")
        for m in missing:
            print(f"   - {m}")
            
    if placeholders:
        print(f"\n⚠️  AVISO: {len(placeholders)} variáveis ainda usam valores de exemplo.")
        
    if not missing and not placeholders:
        print("\n✨ Ambiente perfeitamente configurado!")
    else:
        print("\n💡 Dica: Copie as chaves faltantes do .env.example para o seu .env.")

if __name__ == "__main__":
    audit()