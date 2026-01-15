
# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-11 03:35:00
import sys
import os
import uuid
# Adiciona a raiz ao path
sys.path.append(os.getcwd())

from app.database import SessionLocal, set_tenant
from app.models import Company, Category, Product
from sqlalchemy import text

def verify_rls_public_access():
    print("🛡️ Verificando Acesso Público sob RLS...")
    
    # 1. Setup Data
    db = SessionLocal()
    slug = f"rls-test-{uuid.uuid4().hex[:6]}"
    
    try:
        # Criar empresa
        company = Company(
            name="RLS Test Corp",
            slug=slug,
            owner_email=f"rls-{uuid.uuid4()}@test.com"
        )
        db.add(company)
        db.commit()
        db.refresh(company)
        print(f"   ✅ Empresa criada: {slug} (ID: {company.id})")
        
        # Configurar contexto para criar dados protegidos (Category)
        set_tenant(db, str(company.id))
        
        cat = Category(company_id=company.id, name="RLS Protected Cat")
        db.add(cat)
        db.commit()
        print(f"   ✅ Categoria criada sob proteção RLS.")
        
        db.close()
        
        # 2. Teste de Acesso Público (Simulando o Router)
        # Nova sessão limpa (sem contexto definido ainda)
        db_public = SessionLocal()
        
        # Passo A: Buscar empresa (Deve funcionar sem RLS)
        found_company = db_public.query(Company).filter(Company.slug == slug).first()
        if not found_company:
            print("   ❌ FALHA: Não foi possível encontrar a empresa publicamente.")
            return False
            
        # Passo B: Buscar categoria SEM set_tenant (Deve falhar/retornar vazio se RLS estiver ativo e default deny)
        # Nota: Se o RLS estiver mal configurado, isso retornaria dados. Se bem configurado, retorna vazio.
        # Mas queremos que o router FUNCIONE. O router agora chama set_tenant.
        
        # Vamos simular o CORRETO funcionamento do router
        set_tenant(db_public, str(found_company.id))
        
        categories = db_public.query(Category).filter(Category.company_id == found_company.id).all()
        
        if len(categories) == 1:
            print("   ✅ SUCESSO: Dados recuperados após set_tenant() na sessão pública.")
        else:
            print(f"   ❌ FALHA: set_tenant() não desbloqueou os dados. (Encontrados: {len(categories)})")
            return False
            
        # Passo C: Tentar acessar dados de OUTRA empresa com o contexto da primeira
        # (Validação de isolamento)
        other_slug = f"rls-other-{uuid.uuid4().hex[:6]}"
        other_company = Company(name="Other Corp", slug=other_slug, owner_email=f"other-{uuid.uuid4()}@test.com")
        # Precisamos de uma nova sessão admin para criar a outra empresa e seus dados
        db_admin = SessionLocal()
        db_admin.add(other_company)
        db_admin.commit()
        db_admin.refresh(other_company)
        set_tenant(db_admin, str(other_company.id))
        other_cat = Category(company_id=other_company.id, name="Leaked Cat")
        db_admin.add(other_cat)
        db_admin.commit()
        db_admin.close()
        
        # Voltamos à sessão do primeiro tenant
        # Tenta ler categoria da empresa 2 enquanto autenticado como empresa 1
        leaked = db_public.query(Category).filter(Category.company_id == other_company.id).all()
        
        if len(leaked) == 0:
            print("   ✅ SUCESSO: Isolamento RLS confirmado (Não leu dados do vizinho).")
        else:
            print(f"   🚨 FALHA CRÍTICA: Vazamento de dados detectado! (Leu {len(leaked)} itens do vizinho).")
            return False

        return True

    except Exception as e:
        print(f"   ❌ Erro durante o teste: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    if verify_rls_public_access():
        print("\n✨ RLS Hardening Validado: Público e Isolado.")
        sys.exit(0)
    else:
        sys.exit(1)

