# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-09 23:50:00
import os
from pathlib import Path

def display_directory_tree(start_path, excluded_folders):
    """
    Gera uma representação visual da árvore de diretórios.
    """
    for root, dirs, files in os.walk(start_path):
        # Modifica a lista de diretórios in-place para ignorar pastas indesejadas
        dirs[:] = [d for d in dirs if d not in excluded_folders]
        
        path_parts = Path(root).relative_to(start_path).parts
        depth = len(path_parts)
        indent = '│   ' * depth
        
        folder_name = os.path.basename(root)
        if folder_name == '.':
            print(f'├── mesaflow/')
        else:
            print(f'{indent}├── {folder_name}/')
            
        sub_indent = '│   ' * (depth + 1)
        for filename in files:
            print(f'{sub_indent}├── {filename}')

def run_validation():
    """
    Valida se a TASK-MAINT-01 foi executada corretamente.
    """
    print("🔍 Iniciando validação da TASK-MAINT-01..")
    
    target_ignore_path = Path("ignorar")
    
    # Validação 1: Existência da pasta ignorar
    if not target_ignore_path.exists():
        print("❌ ERRO CRÍTICO: O diretório 'ignorar/' não foi encontrado na raiz.")
        exit(1)
        
    # Validação 2: Limpeza da raiz
    # Procura por arquivos que deveriam ter sido movidos
    root_dir = Path(".")
    for entry in root_dir.iterdir():
        if entry.is_file():
            name_lower = entry.name.lower()
            if name_lower.startswith("temp_") or name_lower.startswith("test_"):
                print(f"❌ ERRO: O arquivo de lixo '{entry.name}' ainda permanece na raiz.")
                exit(1)

    print("\n🌳 Árvore de Diretórios do Projeto (Lixo Oculto):")
    print("=" * 50)
    
    # Lista de pastas a ignorar na visualização da árvore para clareza
    folders_to_skip = [
        'node_modules', 
        'ignorar', 
        '.git', 
        '.next', 
        '__pycache__', 
        'venv', 
        '.venv',
        '.pytest_cache'
    ]
    
    display_directory_tree('.', folders_to_skip)
    
    print("=" * 50)
    print("\n✅ Validação concluída: O repositório está sanitizado e organizado.")
    exit(0)

if __name__ == "__main__":
    run_validation()
