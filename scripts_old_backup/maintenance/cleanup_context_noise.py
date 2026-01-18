# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 20:00:00
import os
import shutil
from pathlib import Path

# Configuração
SOURCE_DIRS = [
    "docs/reports",
    "docs/Prompts"
]
TARGET_DIR = Path("ignorar/limpeza")

# Arquivos que DEVEM ser mantidos (Whitelist)
KEEP_FILES = {
    "FISCAL_PRODUCTION_GO_LIVE.md", # Marco histórico importante
    "System_Persona.xml",           # Identidade Core
    "Next_Session_Prompt.xml",      # O prompt atual de handover
    "ULTIMATE_UI_REPORT.md"         # O estado atual da UI (último teste)
}

# Padrões de arquivos a serem movidos (Blacklist)
MOVE_PATTERNS = [
    "INCIDENT_",           # Relatórios de erros passados
    "FULL_UI_TEST_",       # Relatórios de testes intermediários
    "ULTIMATE_UI_REPORT_", # Análises de testes anteriores
    "Master_Handover",     # Prompts antigos
    "System_Instructions"  # Prompts antigos
]

def cleanup_noise():
    print("🧹 Iniciando Limpeza de Ruído Cognitivo...")
    
    if not TARGET_DIR.exists():
        TARGET_DIR.mkdir(parents=True)
        print(f"📁 Diretório criado: {TARGET_DIR}")

    moved_count = 0

    for source_dir in SOURCE_DIRS:
        path = Path(source_dir)
        if not path.exists(): continue

        for file in path.iterdir():
            if not file.is_file(): continue
            
            # Se estiver na whitelist, pula
            if file.name in KEEP_FILES:
                continue

            # Verifica se corresponde aos padrões de lixo
            should_move = any(pattern in file.name for pattern in MOVE_PATTERNS)
            
            if should_move:
                target_path = TARGET_DIR / file.name
                try:
                    shutil.move(str(file), str(target_path))
                    print(f"   📦 Movido: {file.name}")
                    moved_count += 1
                except Exception as e:
                    print(f"   ❌ Erro ao mover {file.name}: {e}")

    print(f"\n✨ Limpeza concluída. {moved_count} arquivos de contexto obsoleto movidos.")
    print("   A próxima IA terá uma visão limpa do estado atual.")

if __name__ == "__main__":
    cleanup_noise()
