
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 01:00:00
import os
import shutil
from pathlib import Path
# Configuração de Preservação (O que NÃO mover)
SAFE_DIRS = {'app', 'frontend', 'mobile', 'docs', 'scripts', 'alembic', '.git', '.github', 'backups'}
SAFE_FILES = {
    'atualizar.py', 'gerartxt.py', 'run.py', 'requirements.txt', 
    'package.json', 'alembic.ini', 'docker-compose.yml', 'Dockerfile', 
    '.env', '.env.example', '.gitignore', 'pytest.ini', 'vercel.json', 
    'app.json', 'eas.json', 'kernel_journal.jsonl', 'todososarquivos.txt',
    'resposta.txt', 'atualizar.log', 'README.md', 'SECURITY.md'
}
# Padrões de Lixo (O que mover para ignorar/)
TRASH_EXTENSIONS = {'.tmp', '.bak', '.log', '.old', '.temp', '.pyc'}
TRASH_PREFIXES = {'temp_', 'old_', 'copy_', 'test_'}
class ProjectSanitizer:
    def __init__(self):
        self.root = Path(".")
        self.ignore_dir = self.root / "ignorar"
        self.ignore_dir.mkdir(exist_ok=True)
    def visualize(self):
        print("\n📂 ESTRUTURA DO PROJETO (Raiz + Nível 1)")
        print("=" * 60)
        # Lista itens da raiz (ignorando ocultos exceto .env)
        items = sorted([x for x in self.root.iterdir() if not x.name.startswith('.') or x.name == '.env'])
        for item in items:
            if item.is_dir():
                print(f"📁 {item.name}/")
                # Entra apenas no primeiro nível da subpasta
                try:
                    # Lista apenas as pastas do primeiro nível
                    sub_dirs = sorted([x for x in item.iterdir() if x.is_dir()])
                    # Lista apenas os arquivos do primeiro nível
                    sub_files = sorted([x for x in item.iterdir() if x.is_file()])
                    # Mostra a primeira pasta encontrada
                    if sub_dirs:
                        print(f"   ├── 📁 {sub_dirs[0].name}/")
                    # Mostra o primeiro arquivo encontrado
                    if sub_files:
                        print(f"   └── 📄 {sub_files[0].name}")
                    if len(sub_dirs) > 1 or len(sub_files) > 1:
                        print(f"   ... (+ {len(sub_dirs) + len(sub_files) - 2} itens ocultos)")
                except PermissionError:
                    print("   └── 🔒 Acesso Negado")
            else:
                print(f"📄 {item.name}")
        print("=" * 60)
    def sanitize(self):
        print("\n🧹 Iniciando limpeza de arquivos redundantes na raiz...")
        moved_count = 0
        for item in self.root.iterdir():
            # Ignora diretórios protegidos e a própria pasta ignorar
            if item.is_dir() or item.name in SAFE_FILES or item.name == "ignorar":
                continue
            should_move = False
            # Regra 1: Extensões de lixo
            if item.suffix.lower() in TRASH_EXTENSIONS:
                should_move = True
            # Regra 2: Prefixos de rascunho
            if any(item.name.startswith(pre) for pre in TRASH_PREFIXES):
                should_move = True
            # Regra 3: Arquivos .txt que não estão na safe list
            if item.suffix.lower() == '.txt' and item.name not in SAFE_FILES:
                should_move = True
            if should_move:
                dest = self.ignore_dir / item.name
                # Se já existir, renomeia para não sobrescrever
                if dest.exists():
                    dest = self.ignore_dir / f"{item.stem}_{os.urandom(2).hex()}{item.suffix}"
                try:
                    shutil.move(str(item), str(dest))
                    print(f"   📦 Movido: {item.name} -> ignorar/")
                    moved_count += 1
                except Exception as e:
                    print(f"   ❌ Erro ao mover {item.name}: {e}")
        print(f"\n✨ Sanitização concluída. {moved_count} arquivos movidos.")
if __name__ == "__main__":
    sanitizer = ProjectSanitizer()
    sanitizer.visualize()
    # No terminal do VSCode, o usuário pode decidir se limpa agora
    confirm = input("\nDeseja mover os arquivos redundantes da raiz para a pasta 'ignorar'? (s/n): ")
    if confirm.lower() == 's':
        sanitizer.sanitize()
    else:
        print("Operação de limpeza cancelada. Apenas visualização realizada.")

