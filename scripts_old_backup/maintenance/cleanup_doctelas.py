# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-16 06:35:00
import os
from pathlib import Path

# ==============================================================================
# 🧹 DOCTELAS CLEANUP UTILITY
# ==============================================================================
# Remove arquivos de documentação obsoletos gerados por versões anteriores
# do script de geração (nomes genéricos ou duplicados).
# ==============================================================================

DOCS_ROOT = Path("doctelas")

# Lista de arquivos obsoletos conhecidos
OBSOLETE_FILES = [
    "web/Page.md",
    "web/MenuPage.md", # Substituído por ClientMenuPage e AdminMenuPage
    "web/TableidPage.md", # Substituído por WaiterPosPage
    "web/AdminForgot-passwordPage.md", # Substituído por AdminForgotPasswordPage
    "web/AdminReset-passwordPage.md", # Substituído por AdminResetPasswordPage
    "web/AdminCallbackPage.md", # Substituído por AdminPaymentCallbackPage (se renomeado)
    "web/QuickPage.md", # Substituído por QuickPosPage
    "web/FeaturesPage.md", # Substituído por AdminFeaturesPage
    "web/BillingPage.md", # Substituído por AdminBillingPage
    "web/HistoryPage.md", # Substituído por AdminHistoryPage
    "web/FinancialPage.md", # Substituído por AdminFinancialPage
    "web/TrustPage.md", # Substituído por TrustCenterPage
    "web/StatusPage.md", # Substituído por TrustCenterPage (se consolidado) ou mantido
    "web/SecurityPage.md", # Substituído por TrustCenterPage (se consolidado) ou mantido
    "web/KioskPage.md", # Substituído por KioskAttractScreen
    "web/MonitorPage.md", # Substituído por PublicMonitorPage
    "web/Forgot-passwordPage.md",
    "web/Reset-passwordPage.md",
    "web/CallbackPage.md"
]

def cleanup():
    print("🧹 Iniciando limpeza de documentação obsoleta...")
    removed_count = 0
    
    for file_path in OBSOLETE_FILES:
        target = DOCS_ROOT / file_path
        if target.exists():
            try:
                os.remove(target)
                print(f"   🗑️  Removido: {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"   ❌ Erro ao remover {file_path}: {e}")
    
    print(f"\n✨ Limpeza concluída. {removed_count} arquivos removidos.")

if __name__ == "__main__":
    cleanup()

