import os
from pathlib import Path

dirs = ['docs/governance', 'docs/Prompts']
output_file = 'governance_bundle.txt'

print(f"🔍 Agrupando arquivos de: {dirs}...")

with open(output_file, 'w', encoding='utf-8') as out:
    for start_dir in dirs:
        path = Path(start_dir)
        if not path.exists():
            print(f"⚠️  Aviso: Diretorio {start_dir} nao encontrado.")
            continue
            
        for file_path in path.rglob('*'):
            if file_path.is_file() and file_path.suffix in ['.md', '.xml']:
                rel_path = str(file_path).replace('\\', '/')
                try:
                    content = file_path.read_text(encoding='utf-8')
                    out.write(f"[[MESAFLOW_BEGIN:{rel_path}]]\n")
                    out.write(content)
                    out.write(f"\n[[MESAFLOW_END]]\n\n")
                    print(f"   ✅ Incluido: {rel_path}")
                except Exception as e:
                    print(f"   ❌ Erro ao ler {rel_path}: {e}")

print(f"\n✨ Sucesso! Tudo foi salvo em: {output_file}")
