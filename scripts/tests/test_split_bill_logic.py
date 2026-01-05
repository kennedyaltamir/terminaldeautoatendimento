from decimal import Decimal

def calculate_split_equal(total: Decimal, people: int) -> Decimal:
    if people <= 0: return total
    return total / people

def calculate_split_items(items: list) -> Decimal:
    return sum(item['price'] for item in items)

def test_split_bill_logic():
    """
    Testa a lógica de cálculo de divisão de conta que será usada no frontend.
    (Simulação da lógica JS em Python para garantir integridade matemática)
    """
    
    # Caso 1: Divisão Igualitária
    total = Decimal("100.00")
    people = 4
    share = calculate_split_equal(total, people)
    assert share == Decimal("25.00")
    
    # Caso 2: Divisão por Itens
    selected_items = [
        {"name": "Hambúrguer", "price": Decimal("30.00")},
        {"name": "Coca", "price": Decimal("6.00")},
        {"name": "Batata", "price": Decimal("12.00")}
    ]
    share_items = calculate_split_items(selected_items)
    assert share_items == Decimal("48.00")
    
    # Caso 3: Divisão com número ímpar (Dízima)
    # R$ 100 / 3 = 33.333... -> Frontend deve arredondar visualmente, mas a soma deve bater.
    # Aqui testamos apenas a divisão bruta.
    share_odd = calculate_split_equal(Decimal("100.00"), 3)
    assert round(share_odd, 2) == Decimal("33.33")