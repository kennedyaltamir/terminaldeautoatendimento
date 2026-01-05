import os
import shutil

def cleanup():
    print("🧹 Iniciando Limpeza Pré-Deploy...")

    # 1. Arquivos de Teste/Dev Perigosos
    files_to_remove = [
        "force_unlock.py",
        "fix_delivery.py",
        "fix_absolute.py",
        "malware.jpg",
        "test_image.png",
        "resposta.txt",
        "todososarquivos.txt",
        "gerartxt.py",
        "ver_arvore.py",
        "atualizar.py" # Opcional: remover o atualizador se não for mais usar
    ]

    for file in files_to_remove:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✅ Removido: {file}")
            except Exception as e:
                print(f"⚠️  Erro ao remover {file}: {e}")

    # 2. Limpar Cache Python
    print("\n🧹 Limpando __pycache__...")
    for root, dirs, files in os.walk("."):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d))
                
    print("\n✨ Repositório limpo e pronto para Commit & Push!")

if __name__ == "__main__":
    cleanup()