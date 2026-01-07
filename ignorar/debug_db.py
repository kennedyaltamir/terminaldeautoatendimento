import sys
import os
from sqlalchemy import text
from app.database import SessionLocal
from app.models import Company, Employee

def inspect_db():
    db = SessionLocal()
    print("\n🔍 --- INSPEÇÃO DO BANCO DE DADOS ---")

    # 1. Verificar Empresas
    print("\n🏢 ÚLTIMAS 5 EMPRESAS:")
    companies = db.query(Company).order_by(Company.created_at.desc()).limit(5).all()
    for c in companies:
        print(f"   [ID: {c.id}] {c.name} | Slug: {c.slug} | Email: {c.owner_email}")

    # 2. Verificar Funcionários
    print("\n👷 ÚLTIMOS 5 FUNCIONÁRIOS:")
    employees = db.query(Employee).order_by(Employee.created_at.desc()).limit(5).all()
    for e in employees:
        print(f"   [ID: {e.id}] {e.name} | Role: {e.role} | Company ID: {e.company_id}")

    # 3. Verificar se há orfãos (Funcionários sem empresa válida)
    print("\n⚠️ VERIFICAÇÃO DE INTEGRIDADE:")
    orphans = 0
    for e in employees:
        parent = db.query(Company).filter(Company.id == e.company_id).first()
        if not parent:
            print(f"   ❌ ERRO: Funcionário {e.name} (ID {e.id}) aponta para empresa inexistente {e.company_id}")
            orphans += 1
    
    if orphans == 0:
        print("   ✅ Integridade Referencial parece OK.")

    db.close()

if __name__ == "__main__":
    inspect_db()