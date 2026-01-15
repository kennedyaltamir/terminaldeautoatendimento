# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 22:30:00
import sys
import io
import os
from pathlib import Path

# Windows Resilience
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.getcwd())

def verify():
    print("🔍 Verificando Configuração da Integração Fiscal Real...")
    
    provider = os.getenv("FISCAL_PROVIDER")
    env = os.getenv("FISCAL_ENV")
    
    if provider != "focus":
        print(f"⚠️  Aviso: FISCAL_PROVIDER está como '{provider}'. Mude para 'focus' para ativar a integração real.")
        return 0

    print(f"✅ Provedor: {provider}")
    print(f"✅ Ambiente: {env}")

    # Verifica se o arquivo do provedor existe e tem conteúdo real
    provider_file = Path("app/services/fiscal/providers/focus_nfe.py")
    if provider_file.exists():
        content = provider_file.read_text(encoding="utf-8")
        if "https://api.focusnfe.com.br" in content:
            print("✅ Implementação da API Focus NFe detectada.")
        else:
            print("❌ FALHA: O arquivo focus_nfe.py parece estar incompleto ou é um mock.")
            return 1
    else:
        print("❌ FALHA: Arquivo focus_nfe.py não encontrado.")
        return 1

    print("\n✨ Integração Fiscal validada estruturalmente.")
    print("👉 Próximo passo: Configurar FISCAL_TOKEN no .env e testar em Sandbox.")
    return 0

if __name__ == "__main__":
    sys.exit(verify())
