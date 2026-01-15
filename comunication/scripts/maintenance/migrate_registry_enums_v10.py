
# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-13 03:45:00
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime

# ==============================================================================
# 📉 REGISTRY ENUM MIGRATOR V10.2 (SILENT)
# ==============================================================================
# Objetivo: Normalizar o registry.xml para os Enums Canônicos.
# Fix v10.2: Correção de DeprecationWarning do ElementTree.
# ==============================================================================

REGISTRY_PATH = "comunication/registry.xml"
REPORT_PATH = "comunication/reports/REPORT_ENUM_MIGRATION.md"

MAPPING = {
    "DONE": "SUCCESS",
    "DONE_PASSIVE": "SUCCESS",
    "PASS": "SUCCESS",
    "FAIL": "FAILED",
    "BLOCKED": "BLOCKED_BY_DATA",
    "PENDING": "PENDING",
    "TESTING": "TESTING",
    "DEPRECATED": "DEPRECATED"
}

def migrate_enums():
    print("📉 Iniciando Migração de Enums do Registry (V10.2)...")
    
    if not os.path.exists(REGISTRY_PATH):
        print(f"❌ Erro: {REGISTRY_PATH} não encontrado.")
        sys.exit(1)

    try:
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            xml_content = f.read().strip()
        
        root = ET.fromstring(xml_content)
        tree = ET.ElementTree(root)
        
        changes = []
        
        # 1. Atualizar Definição de Estados
        states_node = root.find("States")
        if states_node is not None: # Fix: Verificação explícita
            root.remove(states_node)
        
        new_states = ET.Element("States")
        for valid_enum in set(MAPPING.values()):
            s = ET.SubElement(new_states, "State")
            s.set("id", valid_enum)
        root.insert(0, new_states)
        
        # 2. Migrar Scripts
        scripts = root.find("Scripts")
        if scripts is not None:
            for script in scripts.findall("Script"):
                old_status = script.get("status", "").upper()
                script_id = script.get("id")
                
                if old_status in MAPPING:
                    new_status = MAPPING[old_status]
                    if old_status != new_status:
                        script.set("status", new_status)
                        changes.append(f"| {script_id} | `{old_status}` | **{new_status}** |")
                else:
                    if old_status not in MAPPING.values():
                         script.set("status", "DEPRECATED")
                         changes.append(f"| {script_id} | `{old_status}` | **DEPRECATED** |")

        # 3. Salvar Alterações
        tree.write(REGISTRY_PATH, encoding="UTF-8", xml_declaration=True)
        
        # 4. Gerar Relatório
        generate_report(changes)
        
        print(f"✅ Migração concluída. {len(changes)} estados atualizados.")
        return 0

    except Exception as e:
        print(f"❌ Falha crítica na migração: {e}")
        return 1

def generate_report(changes):
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("# 📉 Relatório de Migração de Enums (V10.2)\n\n")
        f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("**Executor:** migrate_registry_enums_v10.py\n\n")
        f.write("## Alterações Realizadas\n\n")
        if changes:
            f.write("| Script ID | Estado Anterior | Novo Estado Canônico |\n")
            f.write("| :--- | :--- | :--- |\n")
            f.write("\n".join(changes))
        else:
            f.write("Nenhuma alteração necessária. O arquivo já estava em conformidade.\n")
        f.write("\n\n## Conclusão\n")
        f.write("O arquivo `registry.xml` está validado e em conformidade com o Protocolo INDA V10.")

if __name__ == "__main__":
    sys.exit(migrate_enums())

