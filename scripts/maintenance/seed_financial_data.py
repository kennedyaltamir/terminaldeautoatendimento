
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-13 01:30:00
import sys
import os
import uuid
from decimal import Decimal

# Adiciona a raiz ao path para importações do app
sys.path.append(os.getcwd())

from app.database import SessionLocal
from app.models.company import Company
from app.services.ledger_service import LedgerService
from app.models.fintech import FinancialLedger

def seed_financial_scenario():
    db = SessionLocal()
    print("💰 Gerando Cenário de Auditoria Financeira L7...")

    # 1. Garantir que a Hamburgueria do Zé existe e simular conexão com Gateway
    company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
    if not company:
        print("❌ Erro: Empresa 'hamburgueria-ze' não encontrada. Rode 'python scripts/maintenance/seed.py' primeiro.")
        return

    # Simula que a empresa conectou o Mercado Pago
    company.payment_provider = "mercadopago"
    company.payment_credentials = {"access_token": "TEST-TOKEN-L7-PROD"}
    db.commit()

    # 2. Limpar Ledger anterior para garantir um teste limpo e determinístico
    db.query(FinancialLedger).filter(FinancialLedger.company_id == company.id).delete()
    db.commit()

    # 3. Inserir Transações de Exemplo no Ledger Imutável
    print(f"   -> Inserindo transações no Ledger para {company.name}...")
    
    # Caso 1: Transação Perfeita (Matched)
    # Esta transação existe no nosso banco e existirá no Mock do Gateway
    LedgerService.create_entry(
        db, 
        str(company.id), 
        5000, 
        "CREDIT", 
        "payment", 
        "mp-tx-001", 
        "Venda Mesa 1 - Sucesso"
    )
    
    # Caso 2: Transação com Valor Divergente (Mismatch)
    # No Ledger registraremos 100.00, mas o Mock do Gateway retornará outro valor
    LedgerService.create_entry(
        db, 
        str(company.id), 
        10000, 
        "CREDIT", 
        "payment", 
        "mp-tx-002", 
        "Venda Mesa 2 - Erro de Valor"
    )

    # Caso 3: Transação Fantasma (Ghost - Só no Ledger)
    # Transação que o sistema acha que recebeu, mas não consta no Gateway
    LedgerService.create_entry(
        db, 
        str(company.id), 
        2500, 
        "CREDIT", 
        "payment", 
        "ghost-tx-999", 
        "Venda Offline - Não sincronizada"
    )

    db.commit()
    print(f"✨ Cenário financeiro gerado com sucesso. ID Empresa: {company.id}")
    db.close()

if __name__ == "__main__":
    seed_financial_scenario()

 