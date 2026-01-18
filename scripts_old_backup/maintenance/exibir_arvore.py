# canonic/11_exibir_arvore.py
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16
import os
from pathlib import Path

"""
Script 11: Exibe a árvore de diretórios das pastas especificadas.
Pastas monitoradas:
- docs/governance
- comunication/scripts
"""

FOLDERS = [
    Path("docs/governance"),
    Path("comunication/scripts")
]

def print_tree(folder: Path, prefix=""):
    if not folder.exists():
        print(f"[!] Pasta não encontrada: {folder}")
        return
    
    print(f"{prefix}{folder.name}/")
    entries = sorted(folder.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        if entry.is_dir():
            print_tree(entry, prefix + ("    " if is_last else "│   "))
        else:
            print(f"{prefix}{'└── ' if is_last else '├── '}{entry.name}")

def run():
    print("\n=== Árvore de Pastas ===\n")
    for folder in FOLDERS:
        print_tree(folder)
    print("\n=== Fim da Árvore ===\n")

if __name__ == "__main__":
    run()
