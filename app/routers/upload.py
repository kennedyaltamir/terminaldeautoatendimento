# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-08 22:30:00
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.storage_service import storage
from app.routers.auth import get_current_user

router = APIRouter()

# Assinaturas de arquivos (Magic Numbers)
ALLOWED_SIGNATURES = {
    b"\xFF\xD8\xFF": ".jpg",
    b"\x89\x50\x4E\x47": ".png",
    b"RIFF": ".webp"
}

@router.post("/", response_model=dict)
async def upload_image(
    file: UploadFile = File(...),
    current_user: any = Depends(get_current_user) # Exige autenticação
):
    """
    Faz upload de uma imagem com validação de segurança e persistência (S3 ou Local).
    """

    # 1. Ler os primeiros bytes para verificar a assinatura
    header = await file.read(12) 
    await file.seek(0) 

    is_valid = False
    
    for signature in ALLOWED_SIGNATURES.keys():
        if header.startswith(signature):
            is_valid = True
            break

    if not is_valid:
        raise HTTPException(status_code=400, detail="Arquivo inválido ou corrompido. Use JPG, PNG ou WEBP.")

    # 2. Delegar para o serviço de storage
    try:
        url = await storage.upload_file(file)
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
