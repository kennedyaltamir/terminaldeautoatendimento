# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-14 18:20:00
import subprocess
import sys
import os
import time
from datetime import datetime

# ==============================================================================
# 📚 MESAFLOW DOCUMENTATION PROTOCOL ORCHESTRATOR
# ==============================================================================
# Este script executa a cadeia completa de geração de evidências e atualização
# de documentação viva do sistema.
# ==============================================================================

SCRIPTS = [
    {
        "name": "Integridade Sistêmica (SYS-01)",
        "path": "scripts/maintenance/system_integrity_check.py",
        "desc": "Verifica estrutura de pastas e arquivos críticos."
    },
    {
        "name": "Omnisciência & Rotas (QA)",
        "path": "scripts/validation/system_omniscience_probe.py",
        "desc": "Mapeia todas as rotas e testa status HTTP."
    },
    {
        "name": "Interatividade de UI",
        "path": "scripts/validation/ui_interaction_audit.py",
        "desc": "Verifica botões e links mortos no Frontend."
    },
    {
        "name": "Dashboard de Governança",
        "path": "scripts/maintenance/governance_dashboard.py",
        "desc": "Atualiza métricas de qualidade e compliance."
    },
    {
        "name": "Master Readiness Check",
        "path": "scripts/validation/master_readiness_check.py",
        "desc": "Verifica status final dos Quality Gates."
    }
]

def run_step(step):
    print(f"\n🔄 Executando: {step['name']}...")
    print(f"   📄 {step['desc']}")
    
    start = time.time()
    try:
        # Define PYTHONPATH para garantir imports
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        
        result = subprocess.run(
            f"python {step['path']}", 
            shell=True, 
            capture_output=True, 
            text=True,
            env=env,
            encoding='utf-8',
            errors='replace'
        )
        
        duration = time.time() - start
        
        if result.returncode == 0:
            print(f"   ✅ Sucesso ({duration:.2f}s)")
            # Opcional: Mostrar apenas as últimas linhas da saída para não poluir
            lines = result.stdout.strip().split('\n')
            if lines:
                print(f"      └─ {lines[-1]}")
            return True
        else:
            print(f"   ❌ Falha ({duration:.2f}s)")
            print("   --- STDERR ---")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"   💥 Erro de Execução: {e}")
        return False

def main():
    print("========================================================")
    print("📚 MESAFLOW DOCUMENTATION UPDATE PROTOCOL")
    print(f"   Data: {datetime.now().isoformat()}")
    print("========================================================")
    
    success_count = 0
    
    for step in SCRIPTS:
        if run_step(step):
            success_count += 1
            
    print("\n========================================================")
    print(f"🏁 Protocolo Finalizado.")
    print(f"   Scripts Executados: {len(SCRIPTS)}")
    print(f"   Sucessos: {success_count}")
    print(f"   Falhas: {len(SCRIPTS) - success_count}")
    print("========================================================")
    print("👉 Toda a documentação em 'governance/evidence/' foi atualizada.")

if __name__ == "__main__":
    main()

