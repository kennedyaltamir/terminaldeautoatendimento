from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from app.main import app
from app.database import SessionLocal
from app.models import Company, Order, OrderStatus, PaymentStatus, PaymentProvider
from decimal import Decimal
import uuid
import json

client = TestClient(app)

def test_mercadopago_split_payload_structure():
    """
    Verifica se o payload enviado ao Mercado Pago contém a estrutura correta de Split.
    """
    # 1. Setup
    unique_slug = f"split-test-{uuid.uuid4().hex[:6]}"
    db = SessionLocal()
    
    # CORREÇÃO: Configurar payment_provider e credentials para passar na validação do Service
    company = Company(
        name="Split Corp",
        slug=unique_slug,
        owner_email=f"split-{uuid.uuid4().hex[:6]}@test.com",
        payment_provider=PaymentProvider.MERCADO_PAGO,
        payment_credentials={"access_token": "APP_USR-1234567890"},
        marketplace_fee_percentage=Decimal("2.00") # 2% de comissão
    )
    db.add(company)
    db.commit()
    db.refresh(company)

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

    try:
        # 2. Mock do HTTP Client
        # Patch no local exato onde o httpx é usado no provider
        with patch("app.services.payment.providers.mercadopago.httpx.AsyncClient") as MockClientClass:
            # Configura a instância retornada pelo construtor
            mock_client_instance = AsyncMock()
            MockClientClass.return_value = mock_client_instance
            
            # Configura o context manager (__aenter__) para retornar a mesma instância
            mock_client_instance.__aenter__.return_value = mock_client_instance
            
            # Configura o método post explicitamente como AsyncMock
            mock_post = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 201
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
            mock_client_instance.post = mock_post

            from app.services.payment_service import PaymentService
            service = PaymentService()

            import asyncio
            # Executar a função async em contexto síncrono de teste
            result = asyncio.run(service.create_pix_payment(order, company))

            # 4. Verificações
            # Verifica se o método post foi chamado
            assert mock_post.called
            
            # Verifica argumentos
            args, kwargs = mock_post.call_args

            # Verificar URL e Payload
            assert "api.mercadopago.com/v1/payments" in args[0]
            sent_payload = kwargs["json"]
            assert sent_payload["transaction_amount"] == 100.0
            assert sent_payload["application_fee"] == 2.0

            print("✅ Payload de Split validado com sucesso!")

    finally:
        db.close()
