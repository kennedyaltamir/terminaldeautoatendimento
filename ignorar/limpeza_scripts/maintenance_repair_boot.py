# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 16:00:00
import os
import shutil
import re
from pathlib import Path

def repair():
    print("🛠️ MesaFlow Boot Repair Tool - v1.5 (Atomic & Idempotent)")
    print("========================================================")

    # 1. Corrigir sintaxe no api.ts de forma atômica
    api_path = Path("frontend/src/lib/api.ts")
    if api_path.exists():
        print("📝 Sanitizando sintaxe em api.ts...")
        
        content = api_path.read_text(encoding="utf-8")
        
        # Regex: Garante exatamente três pontos antes de options.headers
        # Remove qualquer sequência de pontos (1 ou mais) e substitui por '...'
        new_content = re.sub(r'\.*options\.headers,', '...options.headers,', content)
        
        # Corrige comentários de metadados se ainda existirem como #
        new_content = new_content.replace('# DOMAIN', '// DOMAIN')
        new_content = new_content.replace('# LAST_MODIFIED', '// LAST_MODIFIED')
        
        if content != new_content:
            api_path.write_text(new_content, encoding="utf-8")
            print("✅ api.ts corrigido.")
        else:
            print("ℹ️  api.ts já estava íntegro.")

    # 2. Limpar cache do Next.js (Força recompilação total)
    next_cache = Path("frontend/.next")
    if next_cache.exists():
        print("🧹 Removendo cache .next...")
        try:
            shutil.rmtree(next_cache)
            print("✅ Cache limpo.")
        except Exception as e:
            print(f"⚠️ Falha ao limpar cache (provavelmente em uso): {e}")

    # 3. Validar .env
    env_path = Path(".env")
    if env_path.exists():
        print("🔍 Validando .env...")
        content = env_path.read_text(encoding="utf-8")
        if "psql " in content:
            print("⚠️ Removendo prefixo 'psql' do .env...")
            new_content = content.replace("psql ", "")
            env_path.write_text(new_content, encoding="utf-8")
            print("✅ .env corrigido.")

    print("\n🚀 REPARO CONCLUÍDO.")
    print("Tente rodar 'python run.py' novamente.")

if __name__ == "__main__":
    repair()
