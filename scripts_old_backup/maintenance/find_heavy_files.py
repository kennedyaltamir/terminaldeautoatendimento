
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 06:55:00
import os
from pathlib import Path

def get_dir_size(path):
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    except Exception:
        pass
    return total

def scan_root():
    print("🔍 Rastreando arquivos gigantes na raiz...")
    root = Path(".")
    
    items = []
    for item in root.iterdir():
        # Ignora pastas de sistema que já sabemos que são grandes
        if item.name in ['.venv', 'venv', '.git', 'node_modules']:
            continue
            
        size = 0
        if item.is_file():
            size = item.stat().st_size
        else:
            size = get_dir_size(str(item))
            
        items.append((item.name, size))
    
    # Ordena do maior para o menor
    items.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n{'PASTA/ARQUIVO':<40} | {'TAMANHO (MB)':<15}")
    print("-" * 60)
    
    found_heavy = False
    for name, size in items:
        mb = size / (1024 * 1024)
        if mb > 50: # Mostra apenas maiores que 50MB
            print(f"{name:<40} | {mb:.2f} MB")
            found_heavy = True
            
    if not found_heavy:
        print("✅ Nenhum arquivo gigante óbvio na raiz.")

if __name__ == "__main__":
    scan_root()

