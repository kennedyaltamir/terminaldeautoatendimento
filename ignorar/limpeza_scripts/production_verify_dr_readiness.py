import os
import sys

def verify_dr_readiness():
    print("🔍 Iniciando Auditoria de Prontidão para Desastres (DR Readiness)...")

    # 1. Verificar Existência do Plano Mestre
    plan_path = "docs/enterprise/DR_BCP_PLAN.md"
    if not os.path.exists(plan_path):
        print(f"❌ Plano de DR não encontrado: {plan_path}")
        sys.exit(1)
    print(f"✅ Plano Mestre encontrado: {plan_path}")

    # 2. Verificar Integridade Referencial (Runbooks)
    # O plano estratégico depende de procedimentos táticos. Eles devem existir.
    required_runbooks = [
        "docs/sre/RUNBOOK_DATABASE_FAILOVER.md",
        "docs/sre/RUNBOOK_REDIS_OUTAGE.md",
        "docs/sre/INCIDENT_RESPONSE_PLAN.md"
    ]

    missing_runbooks = []
    for rb in required_runbooks:
        if not os.path.exists(rb):
            print(f"❌ Runbook Tático FALTANDO: {rb}")
            missing_runbooks.append(rb)
        else:
            print(f"✅ Runbook Tático validado: {rb}")

    if missing_runbooks:
        print("🚨 O Plano de DR referencia documentos inexistentes. Auditoria falhou.")
        sys.exit(1)

    # 3. Verificar Conteúdo Crítico no Plano
    with open(plan_path, "r", encoding="utf-8") as f:
        content = f.read()
        keywords = ["RTO", "RPO", "Neon.tech", "Backup", "Comandante do Incidente"]
        
        for kw in keywords:
            if kw not in content:
                print(f"❌ Palavra-chave crítica ausente no plano: '{kw}'")
                sys.exit(1)

    print("\n🏆 DR Readiness Verified: Plan and Runbooks are consistent.")
    sys.exit(0)

if __name__ == "__main__":
    verify_dr_readiness()
