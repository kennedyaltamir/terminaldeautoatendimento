
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 05:50:00
import os
import shutil
from pathlib import Path

# ==============================================================================
# 🚑 EVIDENCE RESTORATION TOOL
# ==============================================================================
# Recupera relatórios movidos acidentalmente para 'ignorar/' para satisfazer
# a auditoria de integridade do Registry.
# ==============================================================================

SOURCE_DIR = Path("ignorar/comunication/reports")
TARGET_DIR = Path("comunication/reports")

def restore():
    print("🚑 Starting Evidence Restoration...")
    
    if not SOURCE_DIR.exists():
        print(f"⚠️  Source directory not found: {SOURCE_DIR}")
        return

    if not TARGET_DIR.exists():
        TARGET_DIR.mkdir(parents=True, exist_ok=True)

    restored_count = 0
    for item in SOURCE_DIR.glob("REPORT_*.md"):
        target_path = TARGET_DIR / item.name
        if not target_path.exists():
            try:
                shutil.copy2(str(item), str(target_path))
                print(f"   ✅ Restored: {item.name}")
                restored_count += 1
            except Exception as e:
                print(f"   ❌ Failed to restore {item.name}: {e}")
        else:
            print(f"   ℹ️  Skipped (Exists): {item.name}")

    print(f"\n✨ Restoration complete. {restored_count} files recovered.")

if __name__ == "__main__":
    restore()

