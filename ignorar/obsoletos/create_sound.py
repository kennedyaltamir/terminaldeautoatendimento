import os
import base64

# Um beep curto em base64 (MP3)
BEEP_B64 = """
SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//NExAAAAANIAAAAAExBTUUzLjEwMKqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//NExAAAAANIAAAAAqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//NExAAAAANIAAAAAqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//NExAAAAANIAAAAAqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq
"""

def create_sound():
    # Caminho para a pasta public do frontend
    public_dir = os.path.join("frontend", "public")
    os.makedirs(public_dir, exist_ok=True)
    
    file_path = os.path.join(public_dir, "notification.mp3")
    
    # Decodifica e salva
    try:
        # Remove cabeçalhos/espaços se houver e decodifica
        # Nota: O base64 acima é um placeholder muito curto que pode não tocar em todos os players,
        # mas serve para parar o 404. Para um som real, o ideal é baixar um arquivo.
        # Vamos criar um arquivo vazio válido ou escrever bytes dummy para enganar o browser por enquanto.
        
        # Melhor abordagem: Criar um arquivo vazio para parar o 404, 
        # mas o ideal é o usuário colocar um arquivo real depois.
        with open(file_path, "wb") as f:
            f.write(b'\xFF\xFB\x90\xC4\x00\x00\x00') # Header MP3 fake mínimo
            
        print(f"✅ Arquivo de som criado em: {file_path}")
        print("ℹ️  Nota: Este é um som mudo/dummy para evitar erro 404. Substitua por um arquivo real se desejar.")
        
    except Exception as e:
        print(f"❌ Erro ao criar som: {e}")

if __name__ == "__main__":
    create_sound()