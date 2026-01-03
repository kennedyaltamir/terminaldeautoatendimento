import httpx
import logging
import os
from app.services.fiscal.interfaces import FiscalProvider
from app.models import Order, Company

logger = logging.getLogger("FocusNFe")

class FocusNFeProvider(FiscalProvider):
    """
    Integração real com a API da Focus NFe v2.
    Documentação: https://focusnfe.com.br/doc
    """
    
    BASE_URL = "https://api.focusnfe.com.br/v2"
    
    async def emit_invoice(self, order: Order, company: Company):
        if not company.fiscal_token:
            return {"status": "error", "message": "Token fiscal não configurado", "provider_reference": None}

        # 1. Montar Payload (Mapeamento de Dados)
        payload = {
            "natureza_operacao": "Venda ao Consumidor",
            "data_emissao": order.created_at.isoformat(),
            "tipo_documento": 1, # Saída
            "finalidade_emissao": 1, # Normal
            "consumidor": {
                "nome": order.customer_name or "Consumidor Final",
                "cpf": None # Em produção, capturar CPF no checkout se necessário
            },
            "items": []
        }

        for item in order.items:
            payload["items"].append({
                "codigo": str(item.product.id),
                "descricao": item.product.name,
                "ncm": item.product.ncm or "21069090", # Default: Preparações alimentícias
                "cfop": item.product.cfop or "5102",   # Default: Venda de mercadoria
                "unidade": "UN",
                "quantidade": item.quantity,
                "valor_unitario": float(item.unit_price),
                "valor_total": float(item.unit_price * item.quantity),
                "icms_origem": "0", # Nacional
                "icms_situacao_tributaria": "102", # Simples Nacional
                "pis_situacao_tributaria": "07", # Isento
                "cofins_situacao_tributaria": "07" # Isento
            })

        # 2. Enviar Request
        # A Focus usa Basic Auth com o token como username
        auth = (company.fiscal_token, "")
        
        async with httpx.AsyncClient() as client:
            try:
                # Usamos o ID do pedido como referência para evitar duplicidade
                response = await client.post(
                    f"{self.BASE_URL}/nfce?ref={order.id}",
                    json=payload,
                    auth=auth,
                    timeout=15.0
                )
                
                data = response.json()
                
                # Focus retorna 200 ou 202 se aceitou processar
                if response.status_code in [200, 202]:
                    status_focus = data.get("status")
                    
                    # Mapeamento de status da Focus para o nosso
                    internal_status = "processing"
                    if status_focus == "autorizado":
                        internal_status = "emitted"
                    elif status_focus == "erro_autorizacao":
                        internal_status = "error"

                    return {
                        "status": internal_status,
                        "message": data.get("status_sefaz") or data.get("mensagem", "Processando"),
                        "provider_reference": data.get("ref"), # Nosso ID devolvido
                        "nfe_key": data.get("chave_nfe"),
                        "nfe_url_pdf": data.get("url_danfe"),
                        "protocol": data.get("protocolo")
                    }
                else:
                    error_msg = data.get("mensagem", "Erro desconhecido na API Fiscal")
                    logger.error(f"Erro Focus NFe: {error_msg}")
                    return {"status": "error", "message": error_msg, "provider_reference": None}

            except Exception as e:
                logger.error(f"Falha de conexão Fiscal: {e}")
                return {"status": "error", "message": "Erro de comunicação com gateway fiscal", "provider_reference": None}

    async def cancel_invoice(self, order: Order, company: Company, reason: str):
        if not order.nfe_key:
             return {"status": "error", "message": "Nota não possui chave para cancelamento"}

        auth = (company.fiscal_token, "")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(
                    f"{self.BASE_URL}/nfce/{order.nfe_key}?justificativa={reason}",
                    auth=auth
                )
                data = response.json()
                
                if response.status_code in [200, 202] and data.get("status") == "cancelado":
                     return {"status": "canceled", "message": "Nota cancelada com sucesso"}
                
                return {"status": "error", "message": data.get("mensagem", "Erro ao cancelar")}
            except Exception as e:
                return {"status": "error", "message": str(e)}