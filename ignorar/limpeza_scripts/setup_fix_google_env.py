import os

def fix():
    print("🔧 Configurando Mock do Google Auth...")
    env_path = ".env"
    
    if not os.path.exists(env_path):
        print("❌ Arquivo .env não encontrado.")
        return

    with open(env_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "NEXT_PUBLIC_GOOGLE_CLIENT_ID" not in content:
        print("   Injetando chave de teste no .env...")
        with open(env_path, "a", encoding="utf-8") as f:
            f.write("\n# Google Auth (Mock para evitar erro 403 no console)\n")
            f.write("NEXT_PUBLIC_GOOGLE_CLIENT_ID=mock_client_id_for_development_123\n")
        print("✅ .env atualizado com sucesso.")
    else:
        print("ℹ️  Variável NEXT_PUBLIC_GOOGLE_CLIENT_ID já existe.")

if __name__ == "__main__":
    fix()
