# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-27 18:21:54
from sqlalchemy.orm import Session
from app.models import Promotion, DiscountType, Company
from decimal import Decimal
from datetime import datetime, timezone
from typing import Optional, Tuple
from uuid import UUID

class PromotionService:
    @staticmethod
    def validate_coupon(
        db: Session, 
        code: str, 
        cart_total: Decimal, 
        company_id: UUID
    ) -> Tuple[bool, str, Optional[Promotion]]:
        """
        Valida se um cupom é aplicável ao carrinho atual.
        Retorna: (is_valid, message, promotion_obj)
        """
        # 1. Buscar Promoção
        # Case insensitive para o código
        promotion = db.query(Promotion).filter(
            Promotion.company_id == company_id,
            Promotion.code.ilike(code),
            Promotion.is_active == True
        ).first()

        if not promotion:
            return False, "Cupom inválido ou não encontrado.", None

        # 2. Validar Datas (Timezone Aware vs Naive Fix)
        # O banco retorna datas com timezone (UTC). datetime.now() é naive.
        # Vamos converter tudo para naive (local) ou tudo para aware (UTC).
        # A abordagem mais segura é garantir que ambos sejam aware se possível, ou remover tzinfo.
        
        now = datetime.now(timezone.utc) # Agora é aware (UTC)

        if promotion.start_date:
            # Se o banco retornou naive (SQLite), assume UTC. Se aware (Postgres), converte.
            start_date = promotion.start_date
            if start_date.tzinfo is None:
                start_date = start_date.replace(tzinfo=timezone.utc)
            
            if now < start_date:
                return False, "Promoção ainda não iniciada.", None
        
        if promotion.end_date:
            end_date = promotion.end_date
            if end_date.tzinfo is None:
                end_date = end_date.replace(tzinfo=timezone.utc)

            if now > end_date:
                return False, "Cupom expirado.", None

        # 3. Validar Limite de Uso
        if promotion.usage_limit is not None and promotion.current_usage >= promotion.usage_limit:
            return False, "Limite de uso do cupom atingido.", None

        # 4. Validar Valor Mínimo
        if cart_total < promotion.min_order_value:
            return False, f"Valor mínimo para este cupom é R$ {promotion.min_order_value:.2f}", None

        return True, "Cupom aplicado com sucesso!", promotion

    @staticmethod
    def calculate_discount(
        promotion: Promotion, 
        cart_total: Decimal, 
        delivery_fee: Decimal = Decimal(0)
    ) -> Decimal:
        """
        Calcula o valor monetário do desconto baseado nas regras.
        Garante que o desconto nunca exceda o total (evita valor negativo).
        """
        discount = Decimal(0)

        if promotion.discount_type == DiscountType.PERCENTAGE:
            discount = cart_total * (promotion.discount_value / Decimal(100))
            # Aplicar teto máximo se existir
            if promotion.max_discount_value and discount > promotion.max_discount_value:
                discount = promotion.max_discount_value

        elif promotion.discount_type == DiscountType.FIXED:
            discount = promotion.discount_value

        elif promotion.discount_type == DiscountType.SHIPPING:
            # Desconto no frete (limitado ao valor do frete)
            discount = min(promotion.discount_value, delivery_fee)
            # Se o valor do desconto for maior que o frete, o desconto é o frete total (grátis)
            # Se a regra for "Frete Grátis", o discount_value deve ser alto ou igual ao frete
            # Assumindo que discount_value para frete é o valor máximo de desconto no frete
            pass

        # Proteção Final: Desconto não pode ser maior que o total do pedido (sem frete ou com frete?)
        # Geralmente desconto incide sobre produtos. Se for frete, incide sobre frete.
        # Vamos assumir que o total passado aqui é o subtotal dos produtos.
        
        if promotion.discount_type == DiscountType.SHIPPING:
             return discount # Retorna o desconto do frete
        
        # Para outros tipos, limita ao valor do carrinho
        return min(discount, cart_total)

    @staticmethod
    def increment_usage(db: Session, promotion_id: UUID):
        """Incrementa o contador de uso da promoção."""
        promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
        if promotion:
            promotion.current_usage += 1
            db.commit()
