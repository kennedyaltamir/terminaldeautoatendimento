# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 18:21:54
from sqlalchemy.orm import Session
from app.models import Order, Company, FiscalStatus
from app.services.fiscal.factory import get_fiscal_provider
import logging

logger = logging.getLogger("FiscalService")

class FiscalService:
    """
    Serviço de alto nível que orquestra a emissão fiscal.
    Executado em Background Task.
    """
    
    @staticmethod
    async def process_emission(order_id: str, company_id: str, db_session_factory):
        """
        Método assíncrono chamado pela BackgroundTask.
        Cria sua própria sessão de banco de dados para thread safety.
        """
        db = db_session_factory()
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            company = db.query(Company).filter(Company.id == company_id).first()
            
            if not order or not company:
                logger.error(f"Pedido {order_id} ou Empresa {company_id} não encontrados no worker.")
                return

            logger.info(f"🧾 Processando emissão fiscal para Pedido #{order.id}...")
            
            # 1. Obter Provedor
            provider = get_fiscal_provider()
            
            # 2. Executar Emissão (Pode demorar)
            result = await provider.emit_invoice(order, company)
            
            # 3. Atualizar Banco de Dados
            if result["status"] == "emitted":
                order.fiscal_status = FiscalStatus.EMITTED
                order.fiscal_reference_id = result.get("provider_reference")
                if "nfe_key" in result: order.nfe_key = result["nfe_key"]
                if "nfe_url_xml" in result: order.nfe_url_xml = result["nfe_url_xml"]
                if "nfe_url_pdf" in result: order.nfe_url_pdf = result["nfe_url_pdf"]
                logger.info(f"✅ NFC-e emitida: {order.nfe_key}")
                
            elif result["status"] == "processing":
                order.fiscal_status = FiscalStatus.PROCESSING
                order.fiscal_reference_id = result.get("provider_reference")
                logger.info(f"⏳ NFC-e em processamento no provedor.")
                
            else:
                order.fiscal_status = FiscalStatus.ERROR
                logger.error(f"❌ Falha NFC-e: {result.get('message')}")
            
            db.commit()
            
        except Exception as e:
            logger.critical(f"🔥 Erro fatal no worker fiscal: {e}")
            db.rollback()
        finally:
            db.close()