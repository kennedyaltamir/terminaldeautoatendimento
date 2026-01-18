import os
import shutil
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 🧹 DEEP AUDIT & CLEANER v1.0 (Industrial Grade)
# ==============================================================================
# 1. Gera a árvore de diretórios filtrada (Deep Scan).
# 2. Move arquivos inúteis/temporários para a pasta 'ignorar/'.
# 3. Mantém a integridade do Kernel e do Source.
# ==============================================================================

IGNORE_DIRS = {
    '.git', '.vscode', '.idea', 'node_modules', 'venv', '.venv', 
    '__pycache__', '.pytest_cache', '.next', 'dist', 'build', 
    '.mesaflow_cache', '.expo'
}

# Arquivos que NUNCA devem ser movidos da raiz
SAFE_ROOT_FILES = {
    'atualizar.py', 'gerartxt.py', 'run.py', 'requirements.txt', 
    'package.json', 'package-lock.json', '.env', '.env.example', 
    '.gitignore', 'alembic.ini', 'docker-compose.yml', 'render.yaml',
    'kernel_journal.jsonl', 'resposta.txt', 'todososarquivos.txt',
    'pytest.ini', 'SECURITY.md', 'readme.md', 'vercel.json', 'app.json', 'eas.json'
}

def generate_tree(startpath, max_depth=3):
    tree = []
    startpath = Path(startpath)
    
    for root, dirs, files in os.walk(startpath):
        # Poda diretórios ignorados
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
        
        rel_path = Path(root).relative_to(startpath)
        depth = len(rel_path.parts)
        
        if depth > max_depth:
            continue
            
        indent = '  ' * depth
        tree.append(f"{indent}📁 {os.path.basename(root)}/")
        
        sub_indent = '  ' * (depth + 1)
        for f in sorted(files):
            if f.startswith('.') and f not in ['.env', '.gitignore']: continue
            tree.append(f"{sub_indent}📄 {f}")
            
    return "\n".join(tree)

def clean_project():
    print("🧹 Iniciando Limpeza Industrial...")
    ignore_path = Path("ignorar")
    ignore_path.mkdir(exist_ok=True)
    
    moved_count = 0
    
    # 1. Limpeza da Raiz
    for item in Path(".").iterdir():
        if item.is_file():
            if item.name not in SAFE_ROOT_FILES and not item.name.startswith('atualizar'):
                # Move arquivos desconhecidos/temporários para ignorar
                dest = ignore_path / item.name
                try:
                    shutil.move(str(item), str(dest))
                    print(f"   🗑️  Movido para ignorar: {item.name}")
                    moved_count += 1
                except: pass

    # 2. Limpeza de Backups Antigos (Mantém apenas os 5 mais recentes)
    backup_dir = Path("backups")
    if backup_dir.exists():
        backups = sorted(list(backup_dir.glob("*.zip")), key=os.path.getmtime)
        if len(backups) > 5:
            for old_backup in backups[:-5]:
                dest = ignore_path / old_backup.name
                shutil.move(str(old_backup), str(dest))
                print(f"   🗑️  Backup antigo arquivado: {old_backup.name}")
                moved_count += 1

    return moved_count

if __name__ == "__main__":
    print("🔍 EXECUTANDO AUDITORIA ESTRUTURAL...")
    current_tree = generate_tree(".")
    
    # Salva a árvore para o usuário enviar
    Path("structure_audit.txt").write_text(current_tree, encoding="utf-8")
    
    print("\n--- ÁRVORE DO PROJETO ---")
    print(current_tree)
    print("\n" + "="*60)
    
    moved = clean_project()
    
    print(f"\n✨ Limpeza concluída. {moved} itens movidos para 'ignorar/'.")
    print("📄 A árvore atualizada foi salva em 'structure_audit.txt'.")