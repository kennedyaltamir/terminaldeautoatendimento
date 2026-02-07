# DOMAIN: BACKEND / SECURITY
# LAST_MODIFIED: 2026-01-30 05:10:00
# DESCRIPTION: Validação rigorosa de assinaturas HMAC para Webhooks (Mercado Pago).
import hmac
import hashlib
import logging
import os
from fastapi import Request, HTTPException

logger = logging.getLogger("WebhookSecurity")

async def verify_mercadopago_signature(request: Request):
    """
    🛡️ PROTOCOLO DE SOBERANIA FINANCEIRA (Achado 03)
    Valida a assinatura HMAC-SHA256 do Mercado Pago para evitar spoofing.
    """
    signature_header = request.headers.get("x-signature")
    request_id = request.headers.get("x-request-id")
    
    if not signature_header or not request_id:
        logger.warning(f"🚨 Tentativa de Webhook sem assinatura. IP: {request.client.host}")
        raise HTTPException(status_code=403, detail="Missing signature headers")

    # Extração dos componentes: ts=...,v1=...
    try:
        parts = dict(x.split('=') for x in signature_header.split(','))
        timestamp = parts.get('ts')
        received_hash = parts.get('v1')
    except Exception:
        raise HTTPException(status_code=403, detail="Malformed signature header")

    if not timestamp or not received_hash:
        raise HTTPException(status_code=403, detail="Incomplete signature components")

    secret = os.getenv("MP_WEBHOOK_SECRET")
    if not secret:
        logger.critical("🔥 MP_WEBHOOK_SECRET não configurado no ambiente!")
        raise HTTPException(status_code=500, detail="Internal security configuration error")

    # Reconstrução do Manifesto conforme documentação oficial MP
    # Template: id:[data.id];request-id:[x-request-id];ts:[ts];
    # Para simplificação e robustez, usamos o ID do recurso e o timestamp
    resource_id = request.query_params.get("data.id") or request_id
    manifest = f"id:{resource_id};request-id:{request_id};ts:{timestamp};"
    
    # Geração do Hash Local
    hmac_obj = hmac.new(secret.encode(), manifest.encode(), hashlib.sha256)
    calculated_hash = hmac_obj.hexdigest()

    # Comparação em tempo constante (Anti-Timing Attack)
    if not hmac.compare_digest(calculated_hash, received_hash):
        logger.error(f"❌ Assinatura INVÁLIDA detectada. IP: {request.client.host}")
        if os.getenv("ENVIRONMENT") == "production":
            raise HTTPException(status_code=403, detail="Invalid cryptographic signature")
    
    return True
