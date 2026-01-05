from decimal import Decimal
from app.services.payment_service import PaymentService

def test_split_calculation_logic():
    service = PaymentService()
    
    # Caso 1: Venda de R$ 100.00 com 1% de taxa
    total = Decimal("100.00")
    fee_percent = Decimal("1.00")
    fee = service.calculate_split(total, fee_percent)
    assert fee == Decimal("1.00")

    # Caso 2: Venda de R$ 28.90 com 2.5% de taxa
    # 28.90 * 0.025 = 0.7225 -> Deve arredondar para 0.72 (Floor)
    total = Decimal("28.90")
    fee_percent = Decimal("2.50")
    fee = service.calculate_split(total, fee_percent)
    assert fee == Decimal("0.72")

    # Caso 3: Taxa Zero
    total = Decimal("50.00")
    fee_percent = Decimal("0.00")
    fee = service.calculate_split(total, fee_percent)
    assert fee == Decimal("0.00")

    # Caso 4: Valor quebrado complexo
    # R$ 33.33 com 10% = 3.333 -> 3.33
    total = Decimal("33.33")
    fee_percent = Decimal("10.00")
    fee = service.calculate_split(total, fee_percent)
    assert fee == Decimal("3.33")