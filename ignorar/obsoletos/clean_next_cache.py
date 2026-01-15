import shutil
import os
import time

def clean_cache():
    print("🧹 Iniciando limpeza de cache do Next.js...")
    
    frontend_path = os.path.join(os.getcwd(), "frontend")
    next_folder = os.path.join(frontend_path, ".next")
    
    if os.path.exists(next_folder):
        try:
            print(f"   Removendo: {next_folder}")
            shutil.rmtree(next_folder)
            print("✅ Cache removido com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao remover cache (pode estar em uso): {e}")
            print("👉 Tente parar o servidor 'python run.py' antes de rodar isso.")
    else:
        print("✨ Cache já estava limpo.")

if __name__ == "__main__":
    clean_cache()
