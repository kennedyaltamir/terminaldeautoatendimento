# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-09 23:50:00
import os
import shutil
import re
import sys
import datetime
import subprocess
import py_compile
from pathlib import Path

# ==============================================================================
# CONFIGURAÇÃO DO EXECUTOR (UEP v3.1)
# ==============================================================================
INPUT_FILE = "resposta.txt"
STAGING_DIR = "Copy"
LOG_FILE = "atualizar.log"

# Arquivos Protegidos (Requer Governance_Override)
PROTECTED_EXACT_FILES = {".env", ".gitignore", "package-lock.json", "yarn.lock", "atualizar.py", "gerartxt.py"}
PROTECTED_DIRECTORIES = ["docs/governance"]

# Padrões de omissão PROIBIDOS (FFP-02)
FORBIDDEN_PATTERNS = [r"\.\.\.", r"restante do código", r"code omitted", r"keep the rest"]

# Ordem Canônica Obrigatória do XML (Atualizado para v6.8 - Inclui Execution_Context)
# A regex foi ajustada para ser mais tolerante a espaços em branco e quebras de linha
CANONICAL_XML_PATTERN = r"<MesaFlow_Execution.*?>\s*<Task_Classification>.*?</Task_Classification>\s*<Domain>.*?</Domain>\s*(?:<Execution_Context>.*?</Execution_Context>\s*)?(?:<Execution_State>.*?</Execution_State>\s*)?(?:<Governance_Override>.*?</Governance_Override>\s*)?<Execution_Result>.*?</Execution_Result>\s*</MesaFlow_Execution>"

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'

def log_action(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {message}\n")

def fail_fast(code, detail, severity="CRITICAL"):
    print(f"\n{Colors.RED}<ERROR code=\"{code}\" severity=\"{severity}\">{Colors.ENDC}")
    print(f"{Colors.YELLOW}{detail}{Colors.ENDC}")
    print(f"{Colors.RED}</ERROR>{Colors.ENDC}")
    log_action(f"ABORT [{code}]: {detail}")
    sys.exit(1)

def is_protected(path_str, allowed_overrides):
    # Se o arquivo estiver na lista de overrides permitidos, libera
    if path_str in allowed_overrides: return False
    
    # Verifica arquivos exatos
    if path_str in PROTECTED_EXACT_FILES: return True
    
    # Verifica diretórios protegidos
    for p_dir in PROTECTED_DIRECTORIES:
        if path_str.startswith(p_dir + "/"): return True
        
    return False

def validate_syntax(path_str, code):
    if path_str.endswith(".py"):
        temp = Path(".temp_syntax.py")
        temp.write_text(code, encoding="utf-8")
        try:
            py_compile.compile(str(temp), doraise=True)
        except Exception as e:
            fail_fast("FFP-05", f"Erro de sintaxe no código proposto para {path_str}: {str(e)}")
        finally:
            if temp.exists(): temp.unlink()

def open_diff_vscode(original_path, proposed_path):
    try:
        abs_orig = str(Path(original_path).resolve())
        abs_new = str(Path(proposed_path).resolve())
        subprocess.Popen(f'code --diff "{abs_orig}" "{abs_new}"', shell=True)
    except Exception as e:
        print(f"{Colors.YELLOW}⚠️  Falha ao abrir Diff: {e}{Colors.ENDC}")

def process_updates():
    input_p = Path(INPUT_FILE)
    if not input_p.exists():
        fail_fast("SYSTEM_ERROR", "Arquivo resposta.txt não encontrado.")

    raw_content = input_p.read_text(encoding="utf-8").strip()

    # 1. Validação Estrutural (Regex Robusto)
    # Removemos a validação estrita de início/fim para permitir comentários antes/depois
    if not re.search(CANONICAL_XML_PATTERN, raw_content, re.DOTALL | re.MULTILINE):
        # Fallback check para dar erro mais descritivo
        if not ("<MesaFlow_Execution" in raw_content and "</MesaFlow_Execution>" in raw_content):
            fail_fast("FFP-01", "RUÍDO DETECTADO: Zero texto permitido fora do envelope XML <MesaFlow_Execution>.")
        fail_fast("FFP-01", "ESTRUTURA INVÁLIDA: O XML não segue a ordem canônica v6.8 (Verifique Execution_Context).")

    # 1. Extração de Overrides (Permissão de Governança)
    # Procura por <Governance_Override>TRUE</Governance_Override> ou lista de arquivos
    has_global_override = "<Governance_Override>TRUE</Governance_Override>" in raw_content
    allowed_overrides = []
    if not has_global_override:
        allowed_overrides = re.findall(r"<File path=\"(.*?)\"/>", raw_content)

    # 2. Parse de Arquivos (Regex Robusto para Non-Raw Input)
    # Aceita [[MESAFLOW_BEGIN:path]] ... [[MESAFLOW_END]]
    file_blocks = re.findall(r"\[\[MESAFLOW_BEGIN:(.*?)\]\](.*?)\[\[MESAFLOW_END\]\]", raw_content, re.DOTALL)

    if not file_blocks:
        print(f"{Colors.BLUE}Status: NO_CHANGE (Nenhum bloco de código encontrado){Colors.ENDC}")
        return

    print(f"{Colors.BLUE}🔍 Auditando Protocolo UEP v3.1...{Colors.ENDC}")

    tasks = []
    for path_str, code in file_blocks:
        path_str = path_str.strip()
        code = code.strip() # Remove quebras de linha extras do copy-paste

        # FFP-02: Omissão
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                fail_fast("FFP-02", f"Omissão de código detectada em {path_str}. Envie o arquivo completo.")

        # FFP-06: Governança
        if not has_global_override and is_protected(path_str, allowed_overrides):
            fail_fast("FFP-06", f"Tentativa de alteração não autorizada em arquivo protegido: {path_str}")

        # FFP-05: Sintaxe
        validate_syntax(path_str, code)

        tasks.append((path_str, code))

    # 3. Execução Segura (Staging -> Diff -> Confirm -> Apply)
    for path_str, code in tasks:
        original_path = Path(path_str)
        staging_path = Path(STAGING_DIR) / path_str

        # A. Gravar na área de Staging (Copy/)
        staging_path.parent.mkdir(parents=True, exist_ok=True)
        staging_path.write_text(code + "\n", encoding="utf-8")

        print(f"\n📄 Processando: {Colors.CYAN}{path_str}{Colors.ENDC}")

        # B. Abrir Diff se o arquivo original existir
        if original_path.exists():
            print(f"   👁️  Abrindo Diff no VS Code...")
            open_diff_vscode(original_path, staging_path)
        else:
            print(f"   ✨ Novo arquivo proposto.")

        # C. Confirmação Interativa
        confirm = input(f"   {Colors.GREEN}>> Aplicar esta alteração? (s/N): {Colors.ENDC}").strip().lower()

        if confirm in ['s', 'sim', 'y', 'yes']:
            # D. Aplicar (Sobrescrever Original)
            original_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(staging_path), str(original_path))
            print(f"   ✅ {Colors.GREEN}Atualizado.{Colors.ENDC}")
            log_action(f"UPDATE: {path_str}")
        else:
            # E. Rejeitar
            print(f"   🚫 {Colors.RED}Ignorado.{Colors.ENDC}")
            log_action(f"SKIP: {path_str}")

    print(f"\n{Colors.BLUE}🏁 Processo finalizado.{Colors.ENDC}")
    print(f"{Colors.YELLOW}ℹ️  Dica: Use o Git para verificar o histórico de alterações.{Colors.ENDC}")

if __name__ == "__main__":
    process_updates()