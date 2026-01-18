import os
import shutil
from pathlib import Path
from datetime import datetime

# ==============================================================================
# CONFIGURAÇÃO DE LIMPEZA DA RAIZ
# ==============================================================================
# Arquivos identificados como temporários, gerados ou binários que não devem
# ficar soltos na raiz do projeto.
TARGETS = [
    "atualizar.log",        # Log de execução
    "auth_state.json",      # Estado de autenticação de testes
    "cd",                   # Arquivo de erro de digitação
    "env.prod",             # Backup de ambiente
    "frontend.env.local",   # Backup de ambiente
    "governance_bundle.txt",# Artefato gerado
    "ngrok.exe",            # Binário solto
    "resposta.txt",         # Buffer de entrada da IA
    "todososarquivos.txt",  # Contexto gerado
    "ver_arvore.py",        # Script utilitário redundante
    "estrutura_atual.txt"   # Relatório da análise anterior
]

# Diretório de destino
DEST_DIR = Path("ignorar") / f"limpeza_raiz_{datetime.now().strftime('%Y%m%d')}"

def cleanup():
    print(f"🧹 Iniciando Varredura Final da Raiz...")
    print(f"📂 Destino: {DEST_DIR}")
    
    if not DEST_DIR.exists():
        DEST_DIR.mkdir(parents=True, exist_ok=True)

    moved_count = 0
    not_found_count = 0

    for filename in TARGETS:
        source = Path(filename)
        if source.exists():
            try:
                destination = DEST_DIR / filename
                shutil.move(str(source), str(destination))
                print(f"   ✅ Movido: {filename}")
                moved_count += 1
            except Exception as e:
                print(f"   ❌ Erro ao mover {filename}: {e}")
        else:
            not_found_count += 1

    print("-" * 50)
    print(f"🏁 Limpeza concluída.")
    print(f"   - Arquivos movidos: {moved_count}")
    print(f"   - Arquivos já limpos/inexistentes: {not_found_count}")
    print(f"   - Localização: {DEST_DIR}")

if __name__ == "__main__":
    cleanup()
