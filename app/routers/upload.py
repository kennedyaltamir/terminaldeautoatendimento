from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import uuid
from pathlib import Path

router = APIRouter()

# Configuração de diretório (Local)
UPLOAD_DIR = Path("frontend/public/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Assinaturas de arquivos (Magic Numbers)
# JPEG: FF D8 FF
# PNG: 89 50 4E 47
# WEBP: RIFF ... WEBP
ALLOWED_SIGNATURES = {
    b"\xFF\xD8\xFF": ".jpg",
    b"\x89\x50\x4E\x47": ".png",
    b"RIFF": ".webp"
}

@router.post("/", response_model=dict)
async def upload_image(file: UploadFile = File(...)):
    """
    Faz upload de uma imagem com validação de segurança (Magic Numbers).
    """
    
    # 1. Ler os primeiros bytes para verificar a assinatura
    header = await file.read(12) # Lê o início do arquivo
    await file.seek(0) # Reseta o cursor para o início para salvar depois

    is_valid = False
    file_ext = ""

    # Verifica se o header começa com alguma assinatura válida
    for signature, ext in ALLOWED_SIGNATURES.items():
        if header.startswith(signature):
            is_valid = True
            file_ext = ext
            break
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Arquivo inválido ou corrompido. Use JPG, PNG ou WEBP reais.")

    # 2. Gerar Nome Único
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename

    # 3. Salvar Arquivo
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar arquivo: {str(e)}")

    # 4. Retornar URL Pública
    return {"url": f"/uploads/{unique_filename}"}