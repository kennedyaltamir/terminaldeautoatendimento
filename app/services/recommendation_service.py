
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models import Order, OrderItem, OrderStatus
from collections import defaultdict

class RecommendationService:
    @staticmethod
    def generate_recommendations(db: Session, company_id: str):
        data = db.query(OrderItem.order_id, OrderItem.product_id).join(Order).filter(
            Order.company_id == company_id,
            Order.status.in_([OrderStatus.DELIVERED, OrderStatus.READY])
        ).all()
        
        if not data: return 0
        
        matrix, counts = RecommendationService._build_matrix(data)
        return RecommendationService._persist_recommendations(db, company_id, matrix, counts)

    @staticmethod
    def _build_matrix(data):
        orders = defaultdict(set)
        counts = defaultdict(int)
        for oid, pid in data:
            orders[oid].add(pid)
            counts[pid] += 1
        
        matrix = defaultdict(lambda: defaultdict(int))
        for pids in orders.values():
            p_list = list(pids)
            for i in range(len(p_list)):
                for j in range(len(p_list)):
                    if i != j: matrix[p_list[i]][p_list[j]] += 1
        return matrix, counts

    @staticmethod
    def _persist_recommendations(db, company_id, matrix, counts):
        db.execute(text("DELETE FROM product_recommendations WHERE source_product_id IN (SELECT id FROM products WHERE category_id IN (SELECT id FROM categories WHERE company_id = :c))"), {"c": company_id})
        total = 0
        for src, targets in matrix.items():
            best = sorted(targets.items(), key=lambda x: x[1]/counts[src], reverse=True)[:3]
            for tgt, score in best:
                db.execute(text("INSERT INTO product_recommendations (source_product_id, target_product_id) VALUES (:s, :t)"), {"s": src, "t": tgt})
                total += 1
        db.commit()
        return total

