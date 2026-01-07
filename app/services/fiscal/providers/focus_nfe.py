import httpx
import logging
import os
from app.services.fiscal.interfaces import FiscalProvider
from app.models import Order, Company, FiscalStatus

logger = logging.getLogger("FocusNFe")

class FocusNFeProvider(FiscalProvider):
    """
    Integração com a API da Focus NFe v2.
    Suporta ambientes Sandbox e Produção via FISCAL_ENV.
    """

    def __init__(self):
        self.env = os.getenv("FISCAL_ENV", "mock").lower()
        if self.env == "sandbox":
            self.base_url = "https://homologacao.focusnfe.com.br/v2"
        else:
            self.base_url = "https://api.focusnfe.com.br/v2"

    async def emit_invoice(self, order: Order, company: Company):
        if not company.fiscal_token:
            return {"status": "error", "message": "Token fiscal não configurado", "provider_reference": None}

        payload = {
            "natureza_operacao": "Venda ao Consumidor",
            "data_emissao": order.created_at.isoformat(),
            "tipo_documento": 1,
            "finalidade_emissao": 1,
            "consumidor": {
                "nome": order.customer_name or "Consumidor Final",
            },
            "items": [
                {
                    "codigo": str(item.product.id),
                    "descricao": item.product.name,
                    "ncm": item.product.ncm or "21069090",
                    "cfop": item.product.cfop or "5102",
                    "unidade": "UN",
                    "quantidade": item.quantity,
                    "valor_unitario": float(item.unit_price),
                    "valor_total": float(item.unit_price * item.quantity),
                    "icms_origem": "0",
                    "icms_situacao_tributaria": "102",
                } for item in order.items
            ]
        }

        auth = (company.fiscal_token, "")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/nfce?ref={order.id}",
                    json=payload,
                    auth=auth,
                    timeout=15.0
                )

                data = response.json()

                if response.status_code in [200, 201, 202]:
                    return self._parse_success(data)

                if response.status_code == 422:
                    if data.get("codigo") == "requisicao_duplicada" or "duplicidade" in data.get("mensagem", "").lower():
                        logger.warning(f"⚠️ Rejeição 204 detectada para Pedido {order.id}. Recuperando nota existente.")
                        return await self._recover_duplicate(client, order.id, auth)

                return {"status": "error", "message": data.get("mensagem", "Erro desconhecido"), "provider_reference": None}

            except Exception as e:
                logger.error(f"Falha de conexão Fiscal: {e}")
                return {"status": "error", "message": "Erro de comunicação com gateway fiscal", "provider_reference": None}

    async def _recover_duplicate(self, client, order_id, auth):
        try:
            response = await client.get(f"{self.base_url}/nfce/{order_id}", auth=auth)
            if response.status_code == 200:
                return self._parse_success(response.json())
        except Exception as e:
            logger.error(f"Erro ao recuperar nota duplicada: {e}")
        
        return {"status": "error", "message": "Pedido duplicado na SEFAZ, mas falha ao recuperar dados originais.", "provider_reference": str(order_id)}

    def _parse_success(self, data):
        status_focus = data.get("status")
        internal_status = "processing"
        if status_focus == "autorizado":
            internal_status = "emitted"
        elif status_focus == "erro_autorizacao":
            internal_status = "error"

        return {
            "status": internal_status,
            "message": data.get("status_sefaz") or data.get("mensagem", "Processando"),
            "provider_reference": data.get("ref"),
            "nfe_key": data.get("chave_nfe"),
            "nfe_url_pdf": data.get("url_danfe"),
            "nfe_url_xml": data.get("url_xml")
        }

    async def cancel_invoice(self, order: Order, company: Company, reason: str):
        """
        Implementação da estrutura de cancelamento via FocusNFe.
        """
        if not order.nfe_key:
            return {"status": "error", "message": "Nota não possui chave para cancelamento"}

        auth = (company.fiscal_token, "")

        async with httpx.AsyncClient() as client:
            try:
                # FocusNFe v2 usa DELETE para cancelamento de NFC-e
                response = await client.delete(
                    f"{self.base_url}/nfce/{order.nfe_key}?justificativa={reason}",
                    auth=auth,
                    timeout=15.0
                )
                data = response.json()

                if response.status_code in [200, 202] and data.get("status") == "cancelado":
                    return {"status": "canceled", "message": "Nota cancelada com sucesso"}

                return {"status": "error", "message": data.get("mensagem", "Erro ao cancelar")}
            except Exception as e:
                logger.error(f"Erro ao cancelar nota {order.nfe_key}: {e}")
                return {"status": "error", "message": str(e)}
