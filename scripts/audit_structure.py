import os
from pathlib import Path

# ==============================================================================
# CONFIGURAÇÃO DE AUDITORIA ESTRUTURAL
# ==============================================================================

# Pastas que serão ignoradas completamente (Ruído)
IGNORE_DIRS = {
    '.git', '.vscode', '.idea', 'node_modules', 'venv', '.venv', 
    '__pycache__', '.pytest_cache', '.next', 'dist', 'build', 
    'coverage', 'android', 'ios', 'ignorar', 'testesvisuais',
    'copy', '.expo'
}

# Arquivos Críticos que DEVEM existir (Baseado no contexto Optimus v9)
CRITICAL_FILES = [
    "docs/governance/OPTIMUS_v9_Architecture.md",
    "docs/TASKS.md",
    "docs/ROADMAP.md",
    "app/main.py",
    "frontend/package.json",
    "mobile/app.json",
    "scripts/automation/optimus_v9_neuro_evolution.py",
    ".env.example",
    "requirements.txt"
]

def print_tree(startpath):
    print(f"\n📂 ESTRUTURA ATUAL DO PROJETO (Filtrada)")
    print("=" * 60)
    
    for root, dirs, files in os.walk(startpath):
        # Filtragem de diretórios in-place
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        
        # Apenas imprime se não for a raiz pura (para formatar melhor)
        if root != startpath:
            print(f"{indent}📁 {os.path.basename(root)}/")
            
        subindent = ' ' * 4 * (level + 1)
        
        # Ordena arquivos para facilitar leitura
        for f in sorted(files):
            # Filtra arquivos de sistema/temp
            if f.startswith('.') and f not in ['.env', '.gitignore', '.env.example']: continue
            if f.endswith('.pyc'): continue
            
            print(f"{subindent}📄 {f}")

def check_missing_critical():
    print(f"\n🔍 VERIFICAÇÃO DE ARQUIVOS CRÍTICOS (Optimus Context)")
    print("=" * 60)
    
    missing_count = 0
    for file_path in CRITICAL_FILES:
        path = Path(file_path)
        if path.exists():
            print(f"✅ Encontrado: {file_path}")
        else:
            print(f"❌ AUSENTE:    {file_path}")
            missing_count += 1
            
    if missing_count > 0:
        print(f"\n⚠️  ATENÇÃO: {missing_count} arquivos críticos estão faltando.")
    else:
        print("\n✨ Todos os arquivos críticos do núcleo estão presentes.")

if __name__ == "__main__":
    # 1. Mostra a árvore limpa
    print_tree('.')
    
    # 2. Verifica o que falta
    check_missing_critical()
