# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 11:10:00
import os
import shutil
from pathlib import Path

def deep_clean():
    print("🧹 Iniciando Faxina Profunda na Raiz (L10 Hygiene)...")
    
    # 1. Mapeamento de Utilitários para Pastas Canônicas
    migration_map = {
        "discover_schema.py": "scripts/governance/discover_schema.py",
        "exibir_arvore.py": "scripts/maintenance/exibir_arvore.py",
        "concat_doctelas.py": "scripts/maintenance/concat_doctelas.py",
        "mesa_scripts_bundle.py": "scripts/maintenance/mesa_scripts_bundle.py",
        "abrirtelas.py": "scripts/maintenance/abrirtelas.py",
        "dev.bat": "scripts/setup/dev.bat"
    }

    for src, dest in migration_map.items():
        if Path(src).exists():
            Path(dest).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(src, dest)
            print(f"   [➔] Movido: {src} -> {dest}")

    # 2. Isolamento de Pastas com Erro de Nome (#)
    junk_folders = ["# scripts", "#ignorar"]
    ignore_base = Path("ignorar/legacy_noise")
    ignore_base.mkdir(parents=True, exist_ok=True)

    for folder in junk_folders:
        if Path(folder).exists():
            try:
                shutil.move(folder, str(ignore_base / folder.replace("# ", "").replace("#", "")))
                print(f"   [!] Pasta ruidosa isolada: {folder}")
            except:
                print(f"   [?] Falha ao mover {folder} (Pode estar aberta em outro programa)")

    # 3. Limpeza de Arquivos Temporários de Contexto
    temp_files = ["todososarquivos.txt", "anotacoes.txt", "auth_state.json"]
    for f in temp_files:
        if Path(f).exists():
            shutil.move(f, str(Path("utilidades") / f))
            print(f"   [x] Arquivo de contexto movido para utilidades: {f}")

    print("\n✨ Raiz do projeto purificada.")
    print("🚀 O próximo 'gerartxt.py' será muito mais rápido e limpo.")

if __name__ == "__main__":
    deep_clean()