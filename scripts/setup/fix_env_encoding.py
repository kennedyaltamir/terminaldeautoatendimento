# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 15:20:00
import os
import sys

def fix_env_file():
    """
    Detecta se o arquivo .env está em encoding ANSI/Windows-1252 
    e o converte para UTF-8 puro para evitar erros de codec.
    """
    env_path = ".env"
    if not os.path.exists(env_path):
        print("❌ Arquivo .env não encontrado.")
        return

    print(f"🔧 Analisando integridade de encoding do arquivo {env_path}...")
    
    try:
        # Tenta ler como UTF-8
        with open(env_path, "rb") as f:
            content = f.read()
        
        try:
            content.decode("utf-8")
            print("✅ O arquivo já está em UTF-8 válido.")
        except UnicodeDecodeError:
            print("⚠️  Detectado encoding incompatível (provavelmente Windows-1252). Convertendo...")
            # Tenta decodificar como Windows-1252 (onde 0xe7 é 'ç')
            decoded_content = content.decode("cp1252", errors="replace")
            
            # Salva como UTF-8 limpo
            with open(env_path, "w", encoding="utf-8") as f:
                f.write(decoded_content)
            print("✨ Arquivo .env convertido para UTF-8 com sucesso.")

    except Exception as e:
        print(f"💥 Erro fatal ao processar arquivo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_env_file()

