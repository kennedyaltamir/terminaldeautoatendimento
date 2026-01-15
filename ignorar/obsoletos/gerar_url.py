import urllib.parse

# 👇 COLOQUE SEUS DADOS REAIS AQUI
usuario = "postgres"
senha = "SuaSenhaCom@Aqui"  # Coloque a senha exata que deu erro
host = "localhost"
porta = "5432"
banco = "mesaflow_db"

# Codifica usuário e senha automaticamente
senha_encoded = urllib.parse.quote_plus(senha)
usuario_encoded = urllib.parse.quote_plus(usuario)

url_final = f"postgresql://{usuario_encoded}:{senha_encoded}@{host}:{porta}/{banco}"

print("\n✅ COPIE E COLE ISSO NO SEU .ENV:")
print(f"DATABASE_URL={url_final}\n")