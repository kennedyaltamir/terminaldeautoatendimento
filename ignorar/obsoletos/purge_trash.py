import os

def purge():
    # Lista de arquivos identificados como lixo na raiz
    trash_files = [
        "Adiciona o diretório raiz ao PATH",
        "python scripts\\update_db_theme.py",
        "arquivo_novo.txt",
        "cls",
        "path",
        "dummy.txt",
        "# ✅ Fase 1",
        "# ✅ Fase 2",
        "# ✅ Fase 3",
        "# 🔄 Fase 5",
        "## 1. Atualize o `atualizar.py` manualmente (Copie e cole no arquivo)",
        "## 2. Arquivos de Contexto (Para você testar o novo script)"
    ]
    
    print("🧹 Iniciando limpeza física de resíduos...")
    for f in trash_files:
        if os.path.exists(f):
            try:
                os.remove(f)
                print(f"  [OK] Removido: {f}")
            except:
                print(f"  [ERRO] Falha ao remover: {f}")
    print("✨ Diretório limpo!")

if __name__ == "__main__":
    purge()
