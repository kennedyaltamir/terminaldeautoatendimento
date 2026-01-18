import os
import sys
import io
from pathlib import Path

# ==============================================================================
# 🕵️ ERROR CONTEXT COLLECTOR (Syntax Safe)
# ==============================================================================
# Objetivo: Coletar arquivos relacionados a erros 404, CORS e React Loops.
# ==============================================================================

# Fix para Windows Unicode
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OUTPUT_FILE = "contexto_erros.txt"

# Lista cirúrgica baseada no REPORT_FULL_SYSTEM_AUDIT.md
TARGET_FILES = [
    # 1. Configuração Global e Rotas
    "app/main.py",                  
    "frontend/src/lib/api.ts",      
    
    # 2. Backend Routers (Para verificar prefixos)
    "app/routers/public/menu.py",
    "app/routers/public/tables.py",
    "app/routers/admin_employees.py",
    
    # 3. Componentes com React Loop
    "frontend/src/components/menu/PublicMonitorView.tsx",
    "frontend/src/app/admin/[slug]/settings/features/page.tsx",
    
    # 4. Páginas com Erro de Fetch/CORS
    "frontend/src/app/admin/[slug]/team/page.tsx",
    "frontend/src/app/admin/[slug]/menu/page.tsx"
]

def collect():
    print(f"🚀 Coletando contexto de erros para: {OUTPUT_FILE}")
    
    found_count = 0
    missing_count = 0
    
    # Construção segura das tags para evitar confusão do parser
    tag_open = "[["
    tag_close = "]]"
    tag_begin = "MESAFLOW_BEGIN:"
    tag_end = "MESAFLOW_END"
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("# CONTEXTO DE ERROS - MESAFLOW\n")
        out.write("# Arquivos selecionados para correção de 404, CORS e React Loops\n\n")
        
        for file_path in TARGET_FILES:
            path = Path(file_path)
            
            if path.exists():
                print(f"   ✅ Lido: {file_path}")
                try:
                    content = path.read_text(encoding="utf-8")
                    
                    # Normaliza caminho usando forward slash
                    clean_path = str(file_path).replace(os.sep, "/")
                    
                    # Monta o cabeçalho e rodapé dinamicamente
                    header = tag_open + tag_begin + clean_path + tag_close + "\n"
                    footer = "\n" + tag_open + tag_end + tag_close + "\n\n"
                    
                    out.write(header)
                    out.write(content)
                    out.write(footer)
                    found_count += 1
                except Exception as e:
                    print(f"   ⚠️ Erro ao ler {file_path}: {e}")
            else:
                print(f"   ❌ Não encontrado: {file_path}")
                missing_count += 1

    print("\n" + "="*40)
    print(f"📊 Resumo da Coleta")
    print(f"   Arquivos Coletados: {found_count}")
    print(f"   Arquivos Ausentes:  {missing_count}")
    print(f"   Saída: {os.path.abspath(OUTPUT_FILE)}")
    print("="*40)

if __name__ == "__main__":
    collect()

