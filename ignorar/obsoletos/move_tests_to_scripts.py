import os
import shutil
from pathlib import Path

def move_tests():
    root_dir = Path(".")
    source_tests = root_dir / "tests"
    target_parent = root_dir / "scripts"
    target_tests = target_parent / "tests"

    print("📦 Iniciando migração da pasta 'tests'...")

    if not source_tests.exists():
        print("⚠️ Pasta 'tests' não encontrada na raiz. Nada a fazer.")
        return

    if not target_parent.exists():
        target_parent.mkdir()

    # Se já existe scripts/tests, precisamos mesclar ou abortar
    if target_tests.exists():
        print(f"ℹ️  A pasta '{target_tests}' já existe. Mesclando arquivos...")
        for item in source_tests.iterdir():
            try:
                if item.is_dir():
                    shutil.copytree(item, target_tests / item.name, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, target_tests / item.name)
                print(f"   -> Movido: {item.name}")
            except Exception as e:
                print(f"   ❌ Erro ao mover {item.name}: {e}")
        
        # Remove a pasta antiga se estiver vazia ou limpa tudo
        shutil.rmtree(source_tests)
    else:
        # Move a pasta inteira
        shutil.move(str(source_tests), str(target_tests))
        print(f"✅ Pasta movida: {source_tests} -> {target_tests}")

    print("\n🎉 Migração concluída!")

if __name__ == "__main__":
    move_tests()