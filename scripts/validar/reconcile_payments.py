# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 01:20:00
import asyncio
import sys
import os
from sqlalchemy import func
# Adiciona a raiz ao path para importações do app
sys.path.append(os.getcwd())
from app.database import SessionLocal
from app.models.company import Company
from app.services.reconciliation_service import ReconciliationService
async def main():
    db = SessionLocal()
    # Filtro robusto: ignora nulos e o valor string 'none' (case-insensitive)
    companies = db.query(Company).filter(
        Company.payment_provider.isnot(None),
        func.lower(Company.payment_provider) != "none"
    ).all()
    print(f"🔍 Iniciando Conciliação para {len(companies)} empresas conectadas...")
    if not companies:
        print("ℹ️ Nenhuma empresa com provedor de pagamento configurado.")
        return
    for company in companies:
        print(f"\n   -> Processando: {company.name} ({company.slug})")
        print(f"      Provedor: {company.payment_provider}")
        report = await ReconciliationService.reconcile_company(db, str(company.id))
        if report.get("status") == "skipped":
            print(f"      ⚠️  PULADO: {report['reason']}")
            continue
        if report.get("status") == "error":
            print(f"      ❌ ERRO: {report['reason']}")
            continue
        # Sumário do Relatório
        print(f"      ✅ MATCHED:   {len(report['matched'])}")
        if report['mismatches']:
            print(f"      💸 DIVERGENTES: {len(report['mismatches'])}")
            for m in report['mismatches']:
                print(f"         - ID {m['id']}: Gateway={m['expected_gateway']} | Ledger={m['found_ledger']}")
        if report['orphans']:
            print(f"      🚨 ÓRFÃOS (Só no Gateway): {len(report['orphans'])}")
            for o in report['orphans']:
                print(f"         - ID {o['external_id']}: R$ {o['amount_cents']/100:.2f}")
        if report['ghosts']:
            print(f"      👻 FANTASMAS (Só no Ledger): {len(report['ghosts'])}")
            for g_id in report['ghosts']:
                print(f"         - ID {g_id}")
    db.close()
    print("\n✨ Processo de conciliação finalizado.")
if __name__ == "__main__":
    asyncio.run(main())

