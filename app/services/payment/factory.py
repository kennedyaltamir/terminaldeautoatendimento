# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-13 01:20:00
from app.models.core import PaymentProvider
from app.services.payment.interfaces import PaymentProviderInterface
from app.services.payment.providers.mercadopago import MercadoPagoProvider
class PaymentFactory:
    """
    Fábrica de Provedores de Pagamento.
    Garante a resolução correta da implementação baseada no Enum ou String.
    """
    @staticmethod
    def get_provider(provider_enum: any) -> PaymentProviderInterface:
        # Normalização para string minúscula para comparação segura
        provider_str = str(provider_enum).lower() if provider_enum else "none"
        if provider_str == "mercadopago":
            return MercadoPagoProvider()
        if provider_str == "none":
            return None
        # Futuros provedores: efi, stripe, pagarme
        raise ValueError(f"Provedor de pagamento não suportado: {provider_enum}")