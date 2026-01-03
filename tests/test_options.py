from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_order_with_options():
    """
    Testa o fluxo completo de um pedido com adicionais.
    Requer que o seed.py tenha sido rodado.
    """
    # 1. Pegar o cardápio para descobrir IDs
    menu_res = client.get("/api/hamburgueria-ze/menu")
    assert menu_res.status_code == 200
    data = menu_res.json()
    
    # Achar o X-Bacon
    xbacon = next(p for cat in data["categories"] for p in cat["products"] if p["name"] == "X-Bacon")
    assert len(xbacon["option_groups"]) > 0
    
    # Achar opção "Bacon Extra"
    grp_add = next(g for g in xbacon["option_groups"] if g["name"] == "Adicionais")
    opt_bacon = next(o for o in grp_add["options"] if o["name"] == "Bacon Extra")
    
    # 2. Criar Pedido com a opção
    payload = {
        "table_id": 1,
        "qr_token": "token-seguro-mesa-1",
        "customer_name": "Tester Options",
        "items": [
            {
                "product_id": xbacon["id"],
                "quantity": 1,
                "selected_options": [opt_bacon["id"]]
            }
        ]
    }
    
    order_res = client.post("/api/hamburgueria-ze/orders", json=payload)
    assert order_res.status_code == 201
    
    # Validar Preço: 28.90 (X-Bacon) + 3.50 (Bacon Extra) = 32.40
    expected_total = 28.90 + 3.50
    assert float(order_res.json()["total_amount"]) == expected_total