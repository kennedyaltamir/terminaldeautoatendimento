
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 03:55:00
import sys
import os
from pathlib import Path
from datetime import datetime

# Adiciona a raiz ao path para importações do app
sys.path.append(os.getcwd())

from app.database import SessionLocal
from app.models.core import (
    PlanTier, CompanySegment, OrderStatus, PaymentStatus, 
    OrderType, OrderOrigin, ProductStation, UserRole, 
    FiscalStatus, LedgerType, PaymentProvider, DiscountType
)
from sqlalchemy import text

# Mapeamento de Tabelas -> Colunas -> Enum de Referência
AUDIT_MAP = {
    "companies": {
        "plan_tier": PlanTier,
        "segment": CompanySegment,
        "payment_provider": PaymentProvider,
    },
    "orders": {
        "status": OrderStatus,
        "payment_status": PaymentStatus,
        "order_type": OrderType,
        "origin": OrderOrigin,
        "fiscal_status": FiscalStatus,
    },
    "employees": {
        "role": UserRole,
    },
    "products": {
        "station": ProductStation,
    },
    "promotions": {
        "discount_type": DiscountType,
    },
    "driver_ledger": {
        "type": LedgerType,
    }
}

REPORT_PATH = Path("docs/reports/ENUM_DRIFT_REPORT.md")

def run_drift_audit():
    print("🔍 Iniciando Auditoria de Drift de Dados (RFC-009/010)...")
    db = SessionLocal()
    findings = []
    total_violations = 0

    try:
        for table, columns in AUDIT_MAP.items():
            for col, enum_class in columns.items():
                # Busca valores únicos na coluna
                query = text(f"SELECT DISTINCT {col} FROM {table} WHERE {col} IS NOT NULL")
                result = db.execute(query).fetchall()
                
                valid_values = [e.value for e in enum_class]
                
                for row in result:
                    val = row[0]
                    is_valid = val in valid_values
                    is_lowercase = val == val.lower() if isinstance(val, str) else True
                    
                    if not is_valid or not is_lowercase:
                        issue = {
                            "table": table,
                            "column": col,
                            "value": val,
                            "reason": "INVALID_VALUE" if not is_valid else "NOT_LOWERCASE"
                        }
                        findings.append(issue)
                        total_violations += 1
                        print(f"   ❌ Falha em {table}.{col}: '{val}' ({issue['reason']})")

        # Gerar Relatório Markdown
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write(f"# 📊 Relatório de Drift de Dados: Enums\n")
            f.write(f"**Data da Auditoria:** {datetime.now().isoformat()}\n")
            f.write(f"**Status:** {'🔴 CRÍTICO' if total_violations > 0 else '🟢 LIMPO'}\n\n")
            
            f.write(f"## Resumo\n")
            f.write(f"- Total de violações detectadas: {total_violations}\n\n")
            
            if total_violations > 0:
                f.write(f"## Detalhamento de Inconsistências\n")
                f.write("| Tabela | Coluna | Valor Encontrado | Motivo |\n")
                f.write("| :--- | :--- | :--- | :--- |\n")
                for issue in findings:
                    f.write(f"| {issue['table']} | {issue['column']} | `{issue['value']}` | {issue['reason']} |\n")
                
                f.write("\n## Ação Recomendada\n")
                f.write("1. Criar script de migração SQL para normalizar os valores para lowercase.\n")
                f.write("2. Mapear valores inválidos para o estado `DEPRECATED` ou `RETIRED` conforme RFC-010.\n")
            else:
                f.write("✨ Nenhum drift detectado. Todos os dados em produção estão em conformidade com a RFC-009.\n")

        print(f"\n✅ Auditoria concluída. Relatório gerado em: {REPORT_PATH}")
        return total_violations == 0

    except Exception as e:
        print(f"❌ Erro durante a auditoria: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = run_drift_audit()
    sys.exit(0 if success else 1)

