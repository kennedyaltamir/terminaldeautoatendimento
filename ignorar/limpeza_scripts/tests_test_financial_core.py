from decimal import Decimal
from app.services.payment_service import PaymentService
import pytest

service = PaymentService()

def test_split_calculation_standard():
    """Testa cálculo padrão de porcentagem"""
    assert service.calculate_split(Decimal("100.00"), Decimal("2.5")) == Decimal("2.50")
    assert service.calculate_split(Decimal("50.00"), Decimal("10.0")) == Decimal("5.00")

def test_split_calculation_rounding():
    """Testa arredondamento para baixo (Floor) para evitar erro de soma"""
    assert service.calculate_split(Decimal("33.33"), Decimal("10.0")) == Decimal("3.33")
    assert service.calculate_split(Decimal("28.90"), Decimal("2.5")) == Decimal("0.72")

def test_split_safety_checks():
    """Testa proteções contra configurações inválidas"""
    assert service.calculate_split(Decimal("100.00"), Decimal("0")) == Decimal("0.00")
    assert service.calculate_split(Decimal("100.00"), Decimal("-5")) == Decimal("0.00")

    # Taxa > 100% (Erro de config) -> Agora retorna 50% como fail-safe
    assert service.calculate_split(Decimal("100.00"), Decimal("150")) == Decimal("50.00")

def test_split_overflow_protection():
    """Testa proteção contra Fee >= Total"""
    assert service.calculate_split(Decimal("100.00"), Decimal("100")) == Decimal("50.00")
