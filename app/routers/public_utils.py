# DOMAIN: BACKEND
# DESCRIPTION: Utilitários públicos com Rate Limit e Semântica REST correta.
import httpx
import re
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Company
from app.core.limiter import limiter # 🛡️ Rate Limiter

router = APIRouter()

@router.get("/check-slug")
def check_slug_availability(
    slug: str = Query(..., min_length=3, max_length=50),
    db: Session = Depends(get_db)
):
    """
    Verifica disponibilidade de slug.
    Retorna 200 (OK) se livre, 409 (Conflict) se ocupado.
    Cache-Control: 30s para evitar flood.
    """
    # 🛡️ Normalização Defensiva
    slug_clean = slug.lower().strip()
    slug_clean = re.sub(r"[^a-z0-9-]", "", slug_clean)

    exists = db.query(Company).filter(Company.slug == slug_clean).first()
    
    if exists:
        # 🛡️ Semântica REST Correta
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este link já está em uso."
        )
    
    return JSONResponse(
        content={"available": True, "slug": slug_clean},
        headers={"Cache-Control": "public, max-age=30"}
    )

@router.get("/consult-cnpj/{cnpj}")
@limiter.limit("5/minute") # 🛡️ Rate Limit: 5 req/min por IP
async def consult_cnpj(request: Request, cnpj: str):
    """
    Consulta CNPJ na BrasilAPI.
    Protegido por Rate Limit para evitar abuso de proxy.
    """
    clean_cnpj = "".join(filter(str.isdigit, cnpj))
    
    if len(clean_cnpj) != 14:
        raise HTTPException(status_code=400, detail="CNPJ inválido")

    async with httpx.AsyncClient() as client:
        try:
            # Timeout agressivo (3s) para não travar workers
            response = await client.get(f"https://brasilapi.com.br/api/cnpj/v1/{clean_cnpj}", timeout=3.0)
            
            if response.status_code != 200:
                # 404 real ou erro da BrasilAPI
                raise HTTPException(status_code=404, detail="CNPJ não encontrado")
            
            data = response.json()
            
            return {
                "name": data.get("nome_fantasia") or data.get("razao_social"),
                "email": data.get("email"),
                "phone": data.get("ddd_telefone_1"),
                "address": {
                    "street": data.get("logradouro"),
                    "number": data.get("numero"),
                    "neighborhood": data.get("bairro"),
                    "city": data.get("municipio"),
                    "state": data.get("uf"),
                    "zip": data.get("cep")
                }
            }
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Serviço de CNPJ indisponível temporariamente")
        except Exception:
            raise HTTPException(status_code=500, detail="Erro interno na consulta")
