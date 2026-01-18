
import os
import shutil
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 🧹 KERNEL JOURNAL ROTATION & RESET
# ==============================================================================
# Objetivo: Arquivar o log atual e iniciar um novo para limpar o Stability Score.
# Uso: Execute quando o sistema estiver estável e os erros antigos forem irrelevantes.
# ==============================================================================

JOURNAL_FILE = Path("kernel_journal.jsonl")
BACKUP_DIR = Path("backups/journals")

def rotate_journal():
    print("🔄 Iniciando Rotação do Kernel Journal...")
    
    if not JOURNAL_FILE.exists():
        print("⚠️  Nenhum journal encontrado para rotacionar.")
        return

    if not BACKUP_DIR.exists():
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = BACKUP_DIR / f"journal_archive_{timestamp}.jsonl"

    try:
        # Move o arquivo atual para o arquivo morto
        shutil.move(str(JOURNAL_FILE), str(archive_path))
        print(f"   📦 Journal antigo arquivado em: {archive_path}")
        
        # Cria um novo journal limpo com o evento de reset
        import json
        import uuid
        
        initial_event = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "session_id": "MAINTENANCE",
            "actor": "SYSTEM",
            "module": "KERNEL",
            "event_type": "JOURNAL_RESET",
            "severity": "INFO",
            "payload": {"reason": "Manual rotation for stability score reset"}
        }
        
        with open(JOURNAL_FILE, "w", encoding="utf-8") as f:
            f.write(json.dumps(initial_event) + "\n")
            
        print(f"   ✨ Novo journal inicializado com sucesso.")
        print(f"   🚀 O Kernel Score no 'otimizar.py' agora deve retornar para 100.")
        
    except Exception as e:
        print(f"   ❌ Falha na rotação: {e}")

if __name__ == "__main__":
    rotate_journal()

