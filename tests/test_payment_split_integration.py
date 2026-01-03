from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, PaymentStatus
from decimal import Decimal
import uuid
import json

client = TestClient(app)

def test_mercadopago_split_payload_structure():
    """
    Verifica se o payload enviado ao Mercado Pago contém a estrutura correta de Split (application_fee).
    Isso garante que o SaaS receba sua comissão.
    """
    # 1. Setup
    unique_slug = f"split-test-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    company = Company(
        name="Split Corp",
        slug=unique_slug,
        owner_email=f"split-{uuid.uuid4().hex[:6]}@test.com",
        mp_access_token="APP_USR-1234567890", # Token Fake
        marketplace_fee_percentage=Decimal("2.00") # 2% de comissão
    )
    db.add(company)
    db.commit()
    db.refresh(company) # Garante que os dados estão carregados
    
    # Pedido de R$ 100.00
    order = Order(
        company_id=company.id,
        customer_name="Split Payer",
        total_amount=Decimal("100.00"),
        status=OrderStatus.PENDING,
        payment_method="online"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # NÃO FECHAR A SESSÃO AQUI para evitar DetachedInstanceError
    # db.close() 

    try:
        # 2. Mock do HTTP Client do Mercado Pago
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            # Configurar o retorno do post
            mock_response = MagicMock()
            mock_response.status_code = 201
            # .json() é um método síncrono no httpx response object
            mock_response.json.return_value = {
                "id": "12345",
                "status": "pending",
                "point_of_interaction": {
                    "transaction_data": {
                        "qr_code": "pix_code_mock",
                        "qr_code_base64": "base64_mock"
                    }
                }
            }
            mock_post.return_value = mock_response

            from app.services.payment_service import PaymentService
            service = PaymentService()
            
            import asyncio
            # Executar a função async em contexto síncrono de teste
            result = asyncio.run(service.create_pix_payment(order, company))
            
            # 4. Verificações
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            
            # Verificar URL
            assert "api.mercadopago.com/v1/payments" in args[0]
            
            # Verificar Payload JSON
            sent_payload = kwargs["json"]
            
            assert sent_payload["transaction_amount"] == 100.0
            # A comissão deve ser 2% de 100 = 2.00
            assert "application_fee" in sent_payload
            assert sent_payload["application_fee"] == 2.0
            
            # Verificar Headers (Token)
            assert kwargs["headers"]["Authorization"] == "Bearer APP_USR-1234567890"
            
            print("✅ Payload de Split validado com sucesso!")
            
    finally:
        db.close() # Fecha a sessão no final