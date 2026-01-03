from sqlalchemy.orm import Session
from app.models import Ingredient, Supplier, Company
from decimal import Decimal
from datetime import datetime

class PurchaseService:
    @staticmethod
    def generate_purchase_suggestion(db: Session, company_id: str):
        """
        Analisa o estoque e sugere compras agrupadas por fornecedor.
        Regra: Se estoque < minimo, sugerir compra para atingir (minimo * 2).
        """
        low_stock_items = db.query(Ingredient).filter(
            Ingredient.company_id == company_id,
            Ingredient.current_stock <= Ingredient.min_stock_alert
        ).all()

        orders_by_supplier = {}

        for item in low_stock_items:
            supplier_id = item.supplier_id or 0 # 0 = Sem fornecedor
            supplier_name = item.supplier.name if item.supplier else "Fornecedor Não Identificado"
            
            if supplier_id not in orders_by_supplier:
                orders_by_supplier[supplier_id] = {
                    "supplier_name": supplier_name,
                    "supplier_phone": item.supplier.phone if item.supplier else None,
                    "items": [],
                    "total_estimated": Decimal(0)
                }
            
            # Cálculo de Reposição
            # Meta: Dobro do mínimo para ter margem de segurança
            target_stock = item.min_stock_alert * Decimal(2)
            quantity_to_buy = target_stock - item.current_stock
            
            # Arredondar para cima se for unidade inteira
            if item.unit == 'un':
                quantity_to_buy = quantity_to_buy.quantize(Decimal("1"))
            
            estimated_cost = quantity_to_buy * item.cost_per_unit

            orders_by_supplier[supplier_id]["items"].append({
                "ingredient_name": item.name,
                "current": item.current_stock,
                "min": item.min_stock_alert,
                "to_buy": quantity_to_buy,
                "unit": item.unit,
                "unit_cost": item.cost_per_unit,
                "total_cost": estimated_cost
            })
            
            orders_by_supplier[supplier_id]["total_estimated"] += estimated_cost

        return list(orders_by_supplier.values())

    @staticmethod
    def generate_html_order(company: Company, order_data: dict) -> str:
        """
        Gera um HTML simples e profissional para impressão da ordem de compra.
        """
        items_html = ""
        for item in order_data["items"]:
            items_html += f"""
            <tr style="border-bottom: 1px solid #eee;">
                <td style="padding: 8px;">{item['ingredient_name']}</td>
                <td style="padding: 8px; text-align: center;">{float(item['to_buy'])} {item['unit']}</td>
                <td style="padding: 8px; text-align: right;">R$ {float(item['unit_cost']):.2f}</td>
                <td style="padding: 8px; text-align: right;">R$ {float(item['total_cost']):.2f}</td>
            </tr>
            """

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ordem de Compra - {order_data['supplier_name']}</title>
            <style>
                body {{ font-family: sans-serif; padding: 40px; color: #333; }}
                .header {{ display: flex; justify-content: space-between; margin-bottom: 40px; border-bottom: 2px solid #333; padding-bottom: 20px; }}
                h1 {{ margin: 0; font-size: 24px; }}
                .meta {{ font-size: 14px; color: #666; }}
                table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                th {{ text-align: left; background: #f9f9f9; padding: 10px; font-size: 12px; text-transform: uppercase; }}
                .total {{ text-align: right; font-size: 18px; font-weight: bold; margin-top: 20px; }}
                .footer {{ margin-top: 50px; font-size: 12px; text-align: center; color: #999; border-top: 1px solid #eee; padding-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div>
                    <h1>Ordem de Compra</h1>
                    <p class="meta">{company.name}</p>
                </div>
                <div style="text-align: right;">
                    <p class="meta">Data: {datetime.now().strftime('%d/%m/%Y')}</p>
                    <p class="meta">Fornecedor: <strong>{order_data['supplier_name']}</strong></p>
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Item</th>
                        <th style="text-align: center;">Qtd. Solicitada</th>
                        <th style="text-align: right;">Custo Unit. (Est.)</th>
                        <th style="text-align: right;">Total (Est.)</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
            </table>

            <div class="total">
                Total Estimado: R$ {float(order_data['total_estimated']):.2f}
            </div>

            <div class="footer">
                Gerado automaticamente pelo sistema MesaFlow.
            </div>
            
            <script>window.print();</script>
        </body>
        </html>
        """