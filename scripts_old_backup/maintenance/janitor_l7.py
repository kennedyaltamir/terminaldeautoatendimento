# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 01:00:00
import os
import shutil
from pathlib import Path

# 🎯 ALVOS DE ELIMINAÇÃO (RUÍDO COGNITIVO)
JUNK_ROOT_FILES = {
    'python', '{rel_path}', '{rel}', 'caminho', 
    'ui_dump.xml', 'ui_fail.xml', 'coletar_mobile.py', 
    'bundle_gov.py', 'atualizar.log'
}

OBSOLETE_SCRIPTS = {
    'scripts/automation/auto_fix_reporter_v2.py',
    'scripts/automation/enterprise_ui_explorer_v4.py',
    'scripts/automation/optimus_v9_neuro_evolution.py',
    'scripts/security/audit_enum_usage.py',
    'scripts/security/audit_enum_usage_v2.py'
}

JUNK_REPORTS = {
    'a', 'falha', 'sucesso', 't04', 't07', 't10', 'verificação_teclado'
}

def run_janitor():
    print("🧹 MESAFLOW JANITOR L7 - Higienização de Contexto")
    print("================================================")
    
    ignore_dir = Path("ignorar")
    ignore_dir.mkdir(exist_ok=True)
    
    moved = 0
    
    # 1. Limpeza da Raiz
    for item in Path(".").iterdir():
        if item.is_file() and item.name in JUNK_ROOT_FILES:
            print(f"   [!] Removendo lixo de raiz: {item.name}")
            shutil.move(str(item), str(ignore_dir / item.name))
            moved += 1

    # 2. Limpeza de Scripts Obsoletos
    for script_path in OBSOLETE_SCRIPTS:
        p = Path(script_path)
        if p.exists():
            print(f"   [!] Arquivando script obsoleto: {p.name}")
            shutil.move(str(p), str(ignore_dir / p.name))
            moved += 1

    # 3. Limpeza de Dumps de XML (O maior vilão de tokens)
    xml_dumps_dir = Path("docs/mobile/reports/dumps")
    if xml_dumps_dir.exists():
        count = 0
        for xml in xml_dumps_dir.glob("*.xml"):
            xml.unlink() # Deleta permanentemente
            count += 1
        print(f"   [!] Expurgados {count} dumps XML obsoletos.")

    # 4. Limpeza de pastas/arquivos de lixo em relatórios
    audit_dir = Path("docs/mobile/reports/login_audit")
    if audit_dir.exists():
        for item in audit_dir.iterdir():
            if item.name in JUNK_REPORTS:
                if item.is_dir(): shutil.rmtree(item)
                else: item.unlink()
                print(f"   [!] Removido ruído de auditoria: {item.name}")

    print("================================================")
    print(f"✨ Limpeza concluída. {moved} arquivos arquivados.")
    print(f"🚀 O contexto agora está pronto para a selagem L7.")

if __name__ == "__main__":
    run_janitor()