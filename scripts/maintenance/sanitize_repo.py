# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-09 23:50:00
import os
import shutil
import time
from pathlib import Path

# Lista de arquivos e pastas que devem permanecer na raiz
SAFE_LIST = {
    "app", 
    "frontend", 
    "mobile", 
    "docs", 
    "scripts", 
    "alembic", 
    ".git", 
    ".github",
    "atualizar.py", 
    "gerartxt.py", 
    "run.py", 
    "gerardoc.py", 
    "gerar_kernel.py",
    "requirements.txt", 
    "package.json", 
    "alembic.ini", 
    "docker-compose.yml", 
    "Dockerfile", 
    ".env", 
    ".gitignore", 
    "pytest.ini", 
    "vercel.json", 
    "app.json", 
    "eas.json", 
    "todososarquivos.txt", 
    "resposta.txt", 
    "atualizar.log", 
    "governance_bundle.txt", 
    "ver_arvore.py", 
    "readme.md", 
    "LICENSE"
}

# Padrões de nomes de arquivos considerados lixo
TRASH_PATTERNS = ["temp_", "old_", ".bak", ".tmp", "test_"]

# Diretório de destino para o lixo digital
IGNORE_DIR = Path("ignorar")

def sanitize_repository():
    """
    Varre a raiz do projeto e move arquivos não essenciais para a pasta ignorar.
    """
    print("🧹 Iniciando sanitização cirúrgica do repositório..")
    
    # Garante a existência da pasta de destino
    if not IGNORE_DIR.exists():
        IGNORE_DIR.mkdir()
        print(f"📁 Diretório '{IGNORE_DIR}' criado com sucesso.")

    root_path = Path(".")
    items_moved = 0

    # Itera sobre todos os itens na raiz
    for item in root_path.iterdir():
        # Ignora a própria pasta de destino
        if item.name == "ignorar":
            continue
            
        # Verifica se o item está na lista de proteção (Safe List)
        # Compara em minúsculo para evitar problemas de case no Windows
        is_safe = False
        for safe_item in SAFE_LIST:
            if item.name.lower() == safe_item.lower():
                is_safe = True
                break
        
        if is_safe:
            continue

        should_move = False
        
        # Critério 1: O nome do arquivo contém padrões de lixo
        for pattern in TRASH_PATTERNS:
            if pattern in item.name.lower():
                should_move = True
                break
        
        # Critério 2: Arquivos de texto (.txt) que não estão na Safe List
        if not should_move and item.suffix == ".txt" and item.name not in SAFE_LIST:
            should_move = True
            
        # Critério 3: Arquivos de log (.log) que não são o log oficial do kernel
        if not should_move and item.suffix == ".log" and item.name != "atualizar.log":
            should_move = True

        # Executa a movimentação se o arquivo for identificado como lixo
        if should_move:
            destination_path = IGNORE_DIR / item.name
            
            # Se o arquivo já existir no destino, adiciona um timestamp para evitar colisão
            if destination_path.exists():
                timestamp = int(time.time())
                destination_path = IGNORE_DIR / f"{timestamp}_{item.name}"
            
            try:
                print(f"📦 Movendo item: {item.name} -> {destination_path}")
                shutil.move(str(item), str(destination_path))
                items_moved += 1
            except Exception as error:
                print(f"❌ Falha ao mover {item.name}: {error}")

    print(f"\n✅ Processo de sanitização finalizado.")
    print(f"📊 Total de itens movidos para '{IGNORE_DIR}': {items_moved}")

if __name__ == "__main__":
    sanitize_repository()
