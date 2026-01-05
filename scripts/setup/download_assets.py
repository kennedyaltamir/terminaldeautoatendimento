import os
import requests

# URL de um vídeo de stock (Cozinha/Restaurante) - Mixkit/Coverr (Royalty Free)
VIDEO_URL = "https://assets.mixkit.co/videos/preview/mixkit-people-working-in-a-busy-restaurant-kitchen-4344-large.mp4"
TARGET_PATH = os.path.join("frontend", "public", "hero-video.mp4")

def download_video():
    print(f"⬇️  Baixando vídeo de background...")
    
    try:
        # Cria a pasta public se não existir
        os.makedirs(os.path.dirname(TARGET_PATH), exist_ok=True)
        
        response = requests.get(VIDEO_URL, stream=True)
        response.raise_for_status()
        
        with open(TARGET_PATH, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(f"✅ Vídeo salvo com sucesso em: {TARGET_PATH}")
        print("   Agora o site carregará o vídeo localmente (sem erro 403).")
        
    except Exception as e:
        print(f"❌ Erro ao baixar vídeo: {e}")
        print("   Solução manual: Baixe qualquer vídeo .mp4, renomeie para 'hero-video.mp4' e coloque em 'frontend/public/'")

if __name__ == "__main__":
    download_video()