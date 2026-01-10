# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 02:20:00
import os
import shutil
from pathlib import Path

def repair():
    print("🛠️ MesaFlow Boot Repair Tool")
    print("============================")

    # 1. Forçar correção de sintaxe no api.ts
    api_path = Path("frontend/src/lib/api.ts")
    if api_path.exists():
        print("📝 Corrigindo sintaxe em api.ts")
        content = api_path.read_text(encoding="utf-8")
        # Substituição agressiva para garantir o spread operator
        new_content = content.replace('options.headers,', 'options.headers,')
        api_path.write_text(new_content, encoding="utf-8")
        print("✅ api.ts sanitizado.")

    # 2. Limpar cache do Next.js
    next_cache = Path("frontend/.next")
    if next_cache.exists():
        print("🧹 Removendo cache .next")
        try:
            shutil.rmtree(next_cache)
            print("✅ Cache limpo.")
        except Exception as e:
            print(f"⚠️ Falha ao limpar cache (provavelmente em uso): {e}")

    # 3. Validar .env
    env_path = Path(".env")
    if env_path.exists():
        print("🔍 Validando .env")
        content = env_path.read_text(encoding="utf-8")
        if "psql " in content:
            print("⚠️ Removendo prefixo 'psql' do .env")
            new_content = content.replace("psql ", "")
            env_path.write_text(new_content, encoding="utf-8")
            print("✅ .env corrigido.")

    print("\n🚀 REPARO CONCLUÍDO.")
    print("Tente rodar 'python run.py' novamente.")

if __name__ == "__main__":
    repair()
