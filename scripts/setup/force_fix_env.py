
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 09:15:00
import os

ENV_FILE = ".env"
KEY = "IFOOD_WEBHOOK_SECRET"
VAL = "default_secret_change_me"

def force_append():
    print(f"🔧 Forçando injeção de {KEY} no {ENV_FILE}...")
    
    # Lê o conteúdo atual
    current_content = ""
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            current_content = f.read()

    # Verifica se já existe uma linha ATIVA (sem # no começo)
    lines = current_content.splitlines()
    active_exists = False
    for line in lines:
        if line.strip().startswith(f"{KEY}="):
            active_exists = True
            print(f"✅ Chave ativa encontrada na linha: '{line.strip()}'")
            break
    
    if not active_exists:
        print("⚠️  Chave não detectada ou comentada. Anexando ao final...")
        with open(ENV_FILE, "a", encoding="utf-8") as f:
            # Garante quebra de linha antes
            if current_content and not current_content.endswith("\n"):
                f.write("\n")
            f.write(f"{KEY}={VAL}\n")
        print("✅ Arquivo .env atualizado com sucesso.")
    else:
        print("ℹ️  Nenhuma alteração necessária.")

if __name__ == "__main__":
    force_append()

