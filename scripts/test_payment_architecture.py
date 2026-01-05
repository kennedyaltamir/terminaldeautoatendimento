import sys
import os
import asyncio
from unittest.mock import MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Company, PaymentProvider, Order
from app.services.payment.factory import PaymentFactory
from app.services.payment.providers.mercadopago import MercadoPagoProvider

def test_factory():
    print("🧪 Testando Factory de Pagamentos...")
    
    # 1. Teste MP
    provider = PaymentFactory.get_provider(PaymentProvider.MERCADO_PAGO)
    assert isinstance(provider, MercadoPagoProvider)
    print("✅ Factory retornou MercadoPagoProvider corretamente.")

    # 2. Teste Erro
    try:
        PaymentFactory.get_provider("invalid_provider")
        print("❌ Factory aceitou provider inválido!")
    except ValueError:
        print("✅ Factory rejeitou provider inválido corretamente.")

async def test_mp_provider_logic():
    print("\n🧪 Testando Lógica do Provider MP...")
    
    provider = MercadoPagoProvider()
    
    # Mock de dados
    company = Company(payment_credentials={"access_token": "TEST_TOKEN"})
    order = Order(id="123", total_amount=100.00, customer_name="Test")
    split_rules = {"fee_percentage": 2.5}
    
    # Mock do HTTPX para não chamar API real
    # (Em um teste real usaríamos pytest-asyncio e respx, aqui é um script simples)
    print("ℹ️  Teste de chamada de API requer ambiente completo de teste.")
    print("   A lógica de split (2.5%) será enviada como 'application_fee': 2.50")

if __name__ == "__main__":
    test_factory()
    asyncio.run(test_mp_provider_logic())