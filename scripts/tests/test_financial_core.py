from decimal import Decimal
from app.services.payment_service import PaymentService
import pytest

service = PaymentService()

def test_split_calculation_standard():
    """Testa cálculo padrão de porcentagem"""
    # R$ 100.00 com 2.5% = R$ 2.50
    assert service.calculate_split(Decimal("100.00"), Decimal("2.5")) == Decimal("2.50")
    
    # R$ 50.00 com 10% = R$ 5.00
    assert service.calculate_split(Decimal("50.00"), Decimal("10.0")) == Decimal("5.00")

def test_split_calculation_rounding():
    """Testa arredondamento para baixo (Floor) para evitar erro de soma"""
    # R$ 33.33 com 10% = 3.333 -> Deve ser 3.33
    assert service.calculate_split(Decimal("33.33"), Decimal("10.0")) == Decimal("3.33")
    
    # R$ 28.90 com 2.5% = 0.7225 -> Deve ser 0.72
    assert service.calculate_split(Decimal("28.90"), Decimal("2.5")) == Decimal("0.72")

def test_split_safety_checks():
    """Testa proteções contra configurações inválidas"""
    # Taxa Zero
    assert service.calculate_split(Decimal("100.00"), Decimal("0")) == Decimal("0.00")
    
    # Taxa Negativa (Erro de config)
    assert service.calculate_split(Decimal("100.00"), Decimal("-5")) == Decimal("0.00")
    
    # Taxa > 100% (Erro de config)
    assert service.calculate_split(Decimal("100.00"), Decimal("150")) == Decimal("0.00")

def test_split_overflow_protection():
    """
    Testa proteção contra Fee >= Total (O MP rejeita se a comissão for tudo).
    Nossa lógica de segurança reduz para 50% se isso acontecer (cenário extremo).
    """
    # Se por algum motivo a taxa for 100%, o sistema deve intervir
    # No código atual, taxa > 100 retorna 0.
    # Mas se a taxa for 100%, o fee seria igual ao total.
    
    # Cenário: Taxa 100% (Configuração válida mas perigosa)
    # O código ajusta para 50% se fee >= total
    assert service.calculate_split(Decimal("100.00"), Decimal("100")) == Decimal("50.00")