# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-14 23:30:00
import httpx
import logging
import os
from typing import Dict, Any
from app.services.fiscal.interfaces import FiscalProvider
from app.models import Order, Company

logger = logging.getLogger("FocusNFe")

class FocusNFeProvider(FiscalProvider):
    """
    Implementação Multi-tenant da API Focus NFe v2.
    Prioriza credenciais específicas de cada empresa (banco de dados).
    """
    def __init__(self):
        self.env = os.getenv("FISCAL_ENV", "sandbox").lower()
        if self.env == "production":
            self.base_url = "https://api.focusnfe.com.br/v2"
        else:
            self.base_url = "https://homologacao.focusnfe.com.br/v2"

    async def emit_invoice(self, order: Order, company: Company) -> Dict[str, Any]:
        """
        Envia o pedido para emissão de NFC-e usando o token específico do cliente.
        """
        # 🛡️ LÓGICA MULTI-TENANT: Prioriza o token do banco de dados
        # Se o cliente não configurou, tenta usar o token global do .env (apenas para testes/plataforma)
        token = company.fiscal_token or os.getenv("FISCAL_TOKEN")

        if not token:
            return {
                "status": "error", 
                "message": "Token fiscal não configurado para esta empresa.",
                "provider_reference": None
            }

        # Payload montado com dados específicos do Tenant (CNPJ, CSC, etc)
        payload = {
            "natureza_operacao": "Venda ao Consumidor",
            "data_emissao": order.created_at.isoformat(),
            "tipo_documento": 1,
            "finalidade_emissao": 1,
            "cnpj_emitente": company.cnpj, # Dado do banco
            "csc_token": company.csc_token, # Dado do banco
            "id_token_csc": company.csc_id, # Dado do banco
            "consumidor": {
                "nome": order.customer_name or "Consumidor Final",
                "cpf": "".join(filter(str.isdigit, order.customer_phone or "")) if order.customer_phone else None
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
                    "icms_situacao_tributaria": "102",
                    "icms_origem": "0",
                } for item in order.items
            ]
        }

        auth = (token, "")
        
        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/nfce?ref={order.id}",
                    json=payload,
                    auth=auth
                )
                data = response.json()
                
                if response.status_code in [200, 201, 202]:
                    return self._parse_response(data)
                
                if response.status_code == 422:
                    if data.get("codigo") == "requisicao_duplicada":
                        return await self._recover_invoice(order.id, auth)
                    
                return {
                    "status": "error",
                    "message": data.get("mensagem", "Erro na Focus NFe"),
                    "provider_reference": None
                }

            except Exception as e:
                logger.error(f"🔥 Falha fiscal multi-tenant: {str(e)}")
                return {"status": "error", "message": "Falha de conexão fiscal", "provider_reference": None}

    async def _recover_invoice(self, order_id: str, auth: tuple) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.base_url}/nfce/{order_id}", auth=auth)
            if res.status_code == 200:
                return self._parse_response(res.json())
            return {"status": "error", "message": "Falha ao recuperar nota."}

    def _parse_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        status_focus = data.get("status")
        internal_status = "processing"
        if status_focus == "autorizado": internal_status = "emitted"
        elif status_focus in ["erro_autorizacao", "cancelado"]: internal_status = "error"

        return {
            "status": internal_status,
            "message": data.get("mensagem") or data.get("status_sefaz", "Processando"),
            "provider_reference": data.get("ref"),
            "nfe_key": data.get("chave_nfe"),
            "nfe_url_pdf": data.get("url_danfe"),
            "nfe_url_xml": data.get("url_xml")
        }

    async def cancel_invoice(self, order: Order, company: Company, reason: str) -> Dict[str, Any]:
        token = company.fiscal_token or os.getenv("FISCAL_TOKEN")
        auth = (token, "")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(f"{self.base_url}/nfce/{order.id}?justificativa={reason}", auth=auth)
                if response.status_code in [200, 202]:
                    return {"status": "canceled", "message": "Cancelado."}
                return {"status": "error", "message": "Erro ao cancelar."}
            except Exception as e:
                return {"status": "error", "message": str(e)}
