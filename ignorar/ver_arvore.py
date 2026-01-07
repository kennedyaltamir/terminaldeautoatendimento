import os

def print_tree(startpath):
    # Pastas para ignorar
    ignore_dirs = {'.git', 'node_modules', '__pycache__', '.next', 'venv', '.venv', 'dist', 'build', '.vscode', '.idea'}
    
    for root, dirs, files in os.walk(startpath):
        # Remove pastas ignoradas da busca
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * (level)
        print(f'{indent}├── {os.path.basename(root)}/')
        subindent = '│   ' * (level + 1)
        for f in files:
            print(f'{subindent}├── {f}')

if __name__ == "__main__":
    print(f"Gerando árvore do projeto: {os.getcwd()}\n")
    print_tree('.')