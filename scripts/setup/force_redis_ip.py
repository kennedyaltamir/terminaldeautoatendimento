
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-14 17:50:00
import os
import sys
import asyncio
from pathlib import Path

# Tenta importar redis
try:
    import redis.asyncio as redis
except ImportError:
    print("❌ Biblioteca 'redis' não instalada.")
    sys.exit(1)

ENV_PATH = Path(".env")

async def test_async_connection(url):
    print(f"🔌 Testando conexão ASYNC com: {url}")
    try:
        client = redis.from_url(
            url, 
            encoding="utf-8", 
            decode_responses=True, 
            socket_connect_timeout=2
        )
        await client.ping()
        await client.close()
        print("   ✨ SUCESSO: Conexão Async estabelecida!")
        return True
    except Exception as e:
        print(f"   ❌ Falha Async: {e}")
        return False

def patch_env_to_ip():
    print("📝 Ajustando .env para usar 127.0.0.1 (Mais estável no Windows)...")
    
    if not ENV_PATH.exists():
        print("   ❌ .env não encontrado.")
        return None

    content = ENV_PATH.read_text(encoding="utf-8")
    new_lines = []
    target_url = "redis://127.0.0.1:6379/0"
    
    for line in content.splitlines():
        if line.startswith("REDIS_URL="):
            new_lines.append(f"REDIS_URL={target_url}")
        else:
            new_lines.append(line)
            
    ENV_PATH.write_text("\n".join(new_lines), encoding="utf-8")
    print(f"   ✅ .env atualizado.")
    return target_url

async def main():
    print("========================================")
    print("🔧 MESAFLOW REDIS IP FIX")
    print("========================================")
    print("O driver Async do Python as vezes falha com 'localhost' no Windows.")
    print("Vamos forçar o uso de '127.0.0.1'.")
    
    new_url = patch_env_to_ip()
    if new_url:
        await test_async_connection(new_url)
        print("\n👉 AGORA: Pare o servidor (CTRL+C) e rode 'python run.py' novamente.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

