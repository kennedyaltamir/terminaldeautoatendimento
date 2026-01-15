# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-15 13:40:00
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company

router = APIRouter()

@router.get("/resolve-domain")
def resolve_domain(host: str, db: Session = Depends(get_db)):
    clean_host = host.split(":")[0]
    
    # RESILIÊNCIA L6: Tratamento para ambiente de desenvolvimento
    if clean_host == "localhost" or clean_host == "127.0.0.1":
        # Retorna a empresa padrão do seed para testes locais
        company = db.query(Company).filter(Company.slug == "hamburgueria-ze").first()
        if company:
            return {"slug": company.slug, "valid": True, "env": "dev_bypass"}

    company = db.query(Company).filter(Company.custom_domain == clean_host).first()
    if not company:
        raise HTTPException(status_code=404, detail="Domínio não encontrado")
    return {"slug": company.slug, "valid": True}

# ... restante do arquivo
