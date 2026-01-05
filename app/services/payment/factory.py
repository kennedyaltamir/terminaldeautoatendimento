from app.models import PaymentProvider
from app.services.payment.interfaces import PaymentProviderInterface
from app.services.payment.providers.mercadopago import MercadoPagoProvider

class PaymentFactory:
    @staticmethod
    def get_provider(provider_enum: PaymentProvider) -> PaymentProviderInterface:
        if provider_enum == PaymentProvider.MERCADO_PAGO:
            return MercadoPagoProvider()
        
        # Futuro: EFI, PAGARME, STRIPE
        
        raise ValueError(f"Provedor de pagamento não suportado: {provider_enum}")