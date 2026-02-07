# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 18:21:54

from sqlalchemy.orm import Session
from app.models import Ingredient, Company
from decimal import Decimal
from datetime import datetime

class PurchaseService:
    @staticmethod
    def generate_purchase_suggestion(db: Session, company_id: str):
        low_stock = db.query(Ingredient).filter(
            Ingredient.company_id == company_id,
            Ingredient.current_stock <= Ingredient.min_stock_alert
        ).all()
        
        orders = {}
        for item in low_stock:
            sup_id = item.supplier_id or 0
            sup_name = item.supplier.name if item.supplier else "Sem Fornecedor"
            if sup_id not in orders:
                orders[sup_id] = {"supplier_name": sup_name, "items": [], "total_estimated": Decimal(0)}
            
            qty = (item.min_stock_alert * 2) - item.current_stock
            cost = qty * item.cost_per_unit
            orders[sup_id]["items"].append({
                "name": item.name, "qty": float(qty), "unit": item.unit, "total": float(cost)
            })
            orders[sup_id]["total_estimated"] += cost
        return list(orders.values())

    @staticmethod
    def generate_html_order(company: Company, order_data: dict) -> str:
        items_rows = "".join([
            f"<tr><td>{i['name']}</td><td>{i['qty']} {i['unit']}</td><td>R$ {i['total']:.2f}</td></tr>"
            for i in order_data["items"]
        ])
        return f"""
        <html>
        <head><style>table{{width:100%; border-collapse:collapse;}} td,th{{border:1px solid #eee; padding:8px;}}</style></head>
        <body>
            <h1>Ordem de Compra: {order_data['supplier_name']}</h1>
            <p>Empresa: {company.name} | Data: {datetime.now().strftime('%d/%m/%Y')}</p>
            <table><thead><tr><th>Item</th><th>Qtd</th><th>Total Est.</th></tr></thead>
            <tbody>{items_rows}</tbody></table>
            <h3>Total: R$ {float(order_data['total_estimated']):.2f}</h3>
            <script>window.print();</script>
        </body></html>
        """

