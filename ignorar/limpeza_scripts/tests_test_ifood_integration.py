import pytest
import json
from unittest.mock import patch, AsyncMock, MagicMock
from app.services.ifood_service import IfoodService
from app.models import Company, Order, OrderOrigin, OrderStatus
from app.database import SessionLocal

@pytest.mark.asyncio
async def test_ifood_order_ingestion():
    """
    Valida se o Middleware iFood converte e injeta um pedido corretamente.
    """
    company_id = "550e8400-e29b-41d4-a716-446655440000"
    external_id = "IFOOD-12345"
    
    # 1. Mock da Empresa no Banco
    mock_company = MagicMock(spec=Company)
    mock_company.id = company_id
    mock_company.name = "Loja Teste iFood"
    mock_company.slug = "loja-teste"
    mock_company.ifood_merchant_id = "merchant_abc"
    mock_company.ifood_token = "token_valido"

    service = IfoodService()

    # 2. Mock da Resposta de Detalhes do Pedido do iFood
    mock_ifood_payload = {
        "id": external_id,
        "customer": {"name": "João iFood", "phone": {"number": "11999999999"}},
        "total": {"subTotal": 50.0, "deliveryFee": 5.0, "orderAmount": 55.0},
        "items": [
            {"externalId": "PROD-001", "name": "Burger iFood", "quantity": 1, "unitPrice": 50.0}
        ],
        "delivery": {"deliveryAddress": {"street": "Rua iFood", "number": "100", "neighborhood": "Centro", "city": "SP"}}
    }

    with patch("app.services.ifood_service.SessionLocal") as mock_session_factory:
        mock_db = MagicMock()
        mock_session_factory.return_value = mock_db
        
        # Configura mocks de query
        mock_db.query.return_value.filter.return_value.first.return_value = None # Pedido não existe
        
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = MagicMock(status_code=200)
            mock_get.return_value.json.return_value = mock_ifood_payload

            # 3. Executar Ingestão
            await service.ingest_order(mock_db, mock_company, external_id, {})

            # 4. Verificações
            # Verifica se tentou adicionar o pedido ao banco
            assert mock_db.add.called
            
            # Captura o objeto Order enviado para o db.add
            added_order = mock_db.add.call_args_list[0][0][0]
            assert isinstance(added_order, Order)
            assert added_order.origin == OrderOrigin.IFOOD
            assert added_order.external_order_id == external_id
            assert float(added_order.total_amount) == 55.0
            assert added_order.customer_name == "João iFood"

            print(f"\n✅ Ingestão iFood validada: Pedido {external_id} convertido com sucesso.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_ifood_order_ingestion())
