from sqlalchemy.orm import Session
from sqlalchemy import func, text
from app.models import Order, OrderItem, Product, product_recommendations, OrderStatus
from collections import defaultdict
import logging

logger = logging.getLogger("RecommendationEngine")

class RecommendationService:
    @staticmethod
    def generate_recommendations(db: Session, company_id: str, min_confidence: float = 0.3, limit: int = 3):
        """
        Analisa o histórico de vendas e gera recomendações automáticas (Market Basket Analysis).

        Algoritmo:
        1. Busca todos os pedidos finalizados da empresa.
        2. Cria matriz de co-ocorrência (Quantas vezes A e B foram comprados juntos).
        3. Calcula confiança: P(B|A) = Count(A & B) / Count(A).
        4. Salva as top 'limit' recomendações para cada produto.
        """
        logger.info(f"🧠 [IA] Iniciando análise de Market Basket para empresa {company_id}...")

        # 1. Buscar itens de pedidos finalizados (Apenas pagos/entregues/prontos)
        # Retorna: [(order_id, product_id), ...]
        results = db.query(OrderItem.order_id, OrderItem.product_id)\
            .join(Order)\
            .filter(
                Order.company_id == company_id,
                Order.status.in_([OrderStatus.DELIVERED, OrderStatus.READY, OrderStatus.ACCEPTED])
            ).all()

        if not results:
            logger.warning("⚠️ [IA] Sem dados históricos suficientes para gerar recomendações.")
            return 0

        # 2. Agrupar produtos por pedido
        orders_map = defaultdict(set)
        product_counts = defaultdict(int)

        for order_id, product_id in results:
            orders_map[order_id].add(product_id)
            product_counts[product_id] += 1

        # 3. Calcular Co-ocorrência
        co_occurrence = defaultdict(lambda: defaultdict(int))

        for products in orders_map.values():
            if len(products) < 2: continue

            # Para cada par de produtos no mesmo pedido
            products_list = list(products)
            for i in range(len(products_list)):
                for j in range(len(products_list)):
                    if i != j:
                        source = products_list[i]
                        target = products_list[j]
                        co_occurrence[source][target] += 1

        # 4. Gerar e Salvar Recomendações
        total_links = 0

        # Limpar recomendações antigas desta empresa (Full Refresh)
        # Subquery para pegar IDs de produtos da empresa
        logger.info("🧹 [IA] Limpando recomendações antigas...")
        db.execute(
            text("""
                DELETE FROM product_recommendations 
                WHERE source_product_id IN (
                    SELECT id FROM products 
                    WHERE category_id IN (
                        SELECT id FROM categories WHERE company_id = :cid
                    )
                )
            """),
            {"cid": company_id}
        )

        logger.info("🔗 [IA] Calculando novas conexões...")
        for source_id, targets in co_occurrence.items():
            source_count = product_counts[source_id]
            if source_count == 0: continue

            # Calcular scores
            candidates = []
            for target_id, joint_count in targets.items():
                if source_id == target_id: continue # Proteção contra self-loop

                confidence = joint_count / source_count
                
                # Log de debug para entender a lógica
                # logger.debug(f"Rule: {source_id} -> {target_id} | Conf: {confidence:.2f} ({joint_count}/{source_count})")

                if confidence >= min_confidence:
                    candidates.append((target_id, confidence))

            # Pegar os top N mais fortes
            candidates.sort(key=lambda x: x[1], reverse=True)
            top_candidates = candidates[:limit]

            # Inserir no banco
            for target_id, score in top_candidates:
                db.execute(
                    text("INSERT INTO product_recommendations (source_product_id, target_product_id) VALUES (:source, :target)"),
                    {"source": source_id, "target": target_id}
                )
                total_links += 1

        db.commit()
        logger.info(f"✅ [IA] Finalizado: {total_links} recomendações geradas com sucesso.")
        return total_links
