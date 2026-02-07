# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 18:21:54
import uuid
import logging
import asyncio
from app.services.fiscal.interfaces import FiscalProvider
from app.models import Order, Company

logger = logging.getLogger("FiscalMock")

class MockProvider(FiscalProvider):
    """
    Simula a emissão fiscal para ambiente de desenvolvimento.
    Retorna sucesso imediato.
    """
    
    async def emit_invoice(self, order: Order, company: Company):
        logger.info(f"🧪 [MOCK] Iniciando emissão NFC-e para Pedido #{order.id}")
        
        # Simula delay de rede
        await asyncio.sleep(1)
        
        # Simula validação básica
        if not company.cnpj:
            return {
                "status": "error", 
                "message": "CNPJ da empresa não configurado (Mock)",
                "provider_reference": None
            }

        # Gera dados fake
        fake_ref = f"mock_ref_{uuid.uuid4().hex[:10]}"
        fake_key = f"352301{uuid.uuid4().int}"[:44]
        
        logger.info(f"✅ [MOCK] NFC-e emitida com sucesso: {fake_key}")

        return {
            "status": "emitted", # Mock é síncrono
            "message": "Nota Fiscal emitida (Ambiente de Teste)",
            "provider_reference": fake_ref,
            "nfe_key": fake_key,
            "nfe_url_xml": f"https://api.mesaflow.com/fiscal/sandbox/{fake_key}.xml",
            "nfe_url_pdf": f"https://api.mesaflow.com/fiscal/sandbox/{fake_key}.pdf"
        }

    async def cancel_invoice(self, order: Order, company: Company, reason: str):
        logger.info(f"🧪 [MOCK] Cancelando NFC-e do Pedido #{order.id}")
        return {
            "status": "canceled",
            "message": "Nota cancelada (Mock)",
            "provider_reference": f"cancel_{order.fiscal_reference_id}"
        }