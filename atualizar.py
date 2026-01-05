import os
import shutil
import re
import subprocess
import datetime
import hashlib
import py_compile
import sys
import argparse
import time
from pathlib import Path

# Tentativa de importar Rich para UI profissional
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False

# ================================
# CONFIGURAÇÕES
# ================================
INPUT_FILE = "resposta.txt"
BACKUP_DIR = "Copy"
TEMP_DIR = ".temp_diff"
TRANSACTION_DIR = ".update_transaction"
LOG_FILE = "atualizar.log"
PROJECT_ROOT = Path.cwd().resolve()

# Padrões de omissão (Ironclad Validation)
FORBIDDEN_PATTERNS = [
    r"restante\s*do\s*código",
    r"code\s*omitted",
    r"omitted\s*for\s*brevity",
    r"\/\/\s*\.\.\.\s*$",
    r"#\s*\.\.\.\s*$",
    r"\.\.\.\s*resto",
    r"keep\s*the\s*rest",
    r"mantém\s*o\s*resto"
]

# ================================
# MOTOR DE VALIDAÇÃO (Protocolo v4.3)
# ================================

def validate_protocol(content):
    """Realiza a auditoria completa do protocolo antes da execução."""
    errors = []

    # 1. Verificar Tags de Início/Fim
    begins = re.findall(r"\[\[MESAFLOW_BEGIN:(.*?)\]\]", content)
    ends = re.findall(r"\[\[MESAFLOW_END\]\]", content)
    if len(begins) != len(ends):
        errors.append(f"Divergência de tags: {len(begins)} BEGIN vs {len(ends)} END.")

    # 2. Verificar Classificação de Task
    if not re.search(r"(TRIVIAL|COMPLEXA)", content.upper()):
        errors.append("Classificação de Task (TRIVIAL/COMPLEXA) não encontrada na resposta.")

    # 3. Verificar Placeholders Proibidos (Ignorando spread operator legítimo)
    # Removemos o spread operator (...props) para evitar falsos positivos
    clean_content = re.sub(r"\.\.\.[a-zA-Z0-9_]+", "", content)
    for p in FORBIDDEN_PATTERNS:
        if re.search(p, clean_content, re.IGNORECASE):
            errors.append(f"Placeholder de omissão detectado: '{p}'")

    # 4. Verificar Ritual de Testes
    has_test_file = any("tests/" in b or "spec.ts" in b for b in begins)
    has_exemption = "[TEST_EXEMPT:" in content.upper()
    if not has_test_file and not has_exemption:
        errors.append("Task sem arquivo de teste e sem justificativa [TEST_EXEMPT].")

    return errors

# ================================
# UTILITÁRIOS DE SISTEMA
# ================================

def get_file_hash(path_str):
    p = Path(path_str).resolve()
    if not p.exists(): return None
    if not p.is_file(): return None # Proteção contra diretórios
    return hashlib.md5(p.read_bytes()).hexdigest()

def get_content_hash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def is_safe_path(path_str):
    try:
        target = (PROJECT_ROOT / path_str).resolve()
        return PROJECT_ROOT in target.parents or target == PROJECT_ROOT
    except: return False

def log_action(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def validate_syntax(path_str, code):
    if not path_str.endswith(".py"): return True
    temp_file = Path(".syntax_tmp.py")
    try:
        temp_file.write_text(code, encoding="utf-8")
        py_compile.compile(str(temp_file), doraise=True)
        temp_file.unlink()
        return True
    except Exception as e:
        if temp_file.exists(): temp_file.unlink()
        return str(e)

def check_manual_edit(path_str):
    p = Path(path_str).resolve()
    if not p.exists(): return False

    try:
        rel_p = p.relative_to(PROJECT_ROOT)
    except ValueError:
        return False

    backup_folder = Path(BACKUP_DIR) / rel_p.parent
    if not backup_folder.exists(): return False

    # CORREÇÃO: Filtrar apenas arquivos para evitar PermissionError com diretórios de mesmo nome
    backups = [b for b in backup_folder.glob(f"{p.stem}*") if b.is_file()]
    backups = sorted(backups, reverse=True)

    if not backups: return False
    return get_file_hash(str(p)) != get_file_hash(str(backups[0]))

def get_next_version_path(original_path_str):
    p = Path(original_path_str)
    target_dir = Path(BACKUP_DIR) / p.parent
    target_dir.mkdir(parents=True, exist_ok=True)
    candidate = target_dir / p.name
    if not candidate.exists(): return str(candidate)
    v = 2
    while True:
        candidate = target_dir / f"{p.stem}_v{v}{p.suffix}"
        if not candidate.exists(): return str(candidate)
        v += 1

# ================================
# OPERAÇÃO PRINCIPAL
# ================================

def process_updates(target_file=None, do_commit=False):
    input_p = Path(INPUT_FILE)
    if not input_p.exists():
        return print(f"❌ Erro: {INPUT_FILE} não encontrado.")

    content = input_p.read_text(encoding="utf-8")

    # --- FASE 1: AUDITORIA DE PROTOCOLO ---
    if HAS_RICH: console.print("\n[bold blue]🔍 Auditando Protocolo v4.3...[/bold blue]")
    protocol_errors = validate_protocol(content)
    
    if protocol_errors:
        if HAS_RICH:
            console.print(Panel.fit("\n".join([f"❌ {e}" for e in protocol_errors]), 
                          title="Falha na Validação de Protocolo", style="bold red"))
        else:
            print("\n".join([f"❌ {e}" for e in protocol_errors]))
        
        # --- MODIFICAÇÃO: PERGUNTA AO USUÁRIO ---
        print("\n🚨 O protocolo foi violado.")
        override = input("   Deseja ignorar os erros e atualizar mesmo assim? (s/n): ")
        if override.lower() != 's':
            print("❌ Operação cancelada.")
            return
        print("⚠️  Forçando execução (Protocol Override)...")

    # --- FASE 2: PARSING ---
    begin_pattern = r"\[\[MESAFLOW_BEGIN:(.*?)\]\]\s*(.*?)\s*\[\[MESAFLOW_END\]\]"
    delete_pattern = r"\[\[MESAFLOW_DELETE:(.*?)\]\]"
    updates = re.findall(begin_pattern, content, re.DOTALL)
    deletions = re.findall(delete_pattern, content)

    auto_tasks = []
    manual_tasks = []

    temp_p = Path(TEMP_DIR)
    if temp_p.exists(): shutil.rmtree(temp_p)
    temp_p.mkdir(exist_ok=True)

    for path_str, raw_code in updates:
        path_str = path_str.strip()
        if target_file and target_file not in path_str: continue
        if not is_safe_path(path_str): continue

        p = (PROJECT_ROOT / path_str).resolve()
        clean_code = raw_code.strip()
        if clean_code.startswith("```"):
            clean_code = "\n".join(clean_code.splitlines()[1:-1])

        code_with_newline = clean_code + "\n"

        # Checksum
        if p.exists() and get_file_hash(str(p)) == get_content_hash(code_with_newline):
            continue

        # Sintaxe
        syntax = validate_syntax(path_str, code_with_newline)
        if syntax is not True:
            print(f"❌ Erro de sintaxe em {path_str}: {syntax}")
            continue

        task = {'type': 'WRITE', 'path': path_str, 'code': code_with_newline}

        if p.exists():
            diff_p = temp_p / f"new_{hash(path_str)%1000}_{p.name}"
            diff_p.write_text(code_with_newline, encoding="utf-8")
            subprocess.Popen(['code', '--diff', str(p), str(diff_p)], shell=True)
            task['warning'] = "[bold red]⚠️ Editado Manualmente![/bold red]" if check_manual_edit(path_str) else ""
            manual_tasks.append(task)
        else:
            auto_tasks.append(task)

    for path_str in deletions:
        if Path(path_str).exists():
            manual_tasks.append({'type': 'DELETE', 'path': path_str})

    if not auto_tasks and not manual_tasks:
        if temp_p.exists(): shutil.rmtree(temp_p)
        return print("✨ Nada a ser feito (arquivos idênticos ou filtrados).")

    # --- FASE 3: EXECUÇÃO ---
    if auto_tasks:
        if HAS_RICH: console.print("\n[bold green]✨ Criando novos arquivos automaticamente...[/bold green]")
        for task in auto_tasks:
            p = Path(task['path'])
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(task['code'], encoding="utf-8", newline='\n')
            copy_p = Path(BACKUP_DIR) / task['path']
            copy_p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(p), str(copy_p))
            print(f"  [NEW] {task['path']}")
            log_action(f"CREATE: {task['path']}")

    if manual_tasks:
        if HAS_RICH:
            table = Table(title="Alterações Pendentes")
            table.add_column("Ação", style="cyan")
            table.add_column("Arquivo", style="magenta")
            table.add_column("Aviso", style="yellow")
            for t in manual_tasks: table.add_row(t['type'], t['path'], t.get('warning', ""))
            console.print(table)

        confirm = input("\n🚀 Analise as abas de Diff no VS Code. Confirmar alterações? (s/n): ")
        if confirm.lower() == 's':
            trans_p = Path(TRANSACTION_DIR)
            trans_p.mkdir(exist_ok=True)
            try:
                for task in manual_tasks:
                    p = Path(task['path'])
                    shutil.copy2(str(p), str(trans_p / task['path'].replace(os.sep, "_").replace("/", "_")))
                    if task['type'] == 'WRITE':
                        shutil.copy2(str(p), get_next_version_path(task['path']))
                        p.write_text(task['code'], encoding="utf-8", newline='\n')
                        print(f"  [UPD] {task['path']}")
                        log_action(f"UPDATE: {task['path']}")
                    elif task['type'] == 'DELETE':
                        shutil.copy2(str(p), get_next_version_path(task['path']))
                        p.unlink()
                        print(f"  [DEL] {task['path']}")
                        log_action(f"DELETE: {task['path']}")
                print("\n🎉 Sucesso!")
            except Exception as e:
                print(f"🔥 Erro: {e}. Revertendo...")
                for f in trans_p.iterdir():
                    orig = f.name.replace("_", os.sep)
                    shutil.copy2(str(f), orig)
            finally:
                if trans_p.exists(): shutil.rmtree(trans_p)

    if temp_p.exists(): shutil.rmtree(temp_p)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rollback", action="store_true")
    parser.add_argument("--file", type=str)
    args = parser.parse_args()
    process_updates(target_file=args.file)