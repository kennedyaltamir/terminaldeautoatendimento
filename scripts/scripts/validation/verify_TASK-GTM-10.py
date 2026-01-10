# DOMAIN: DEVOPS_SCRIPTS
import sys
import os
import uuid
from unittest.mock import patch, MagicMock

# Adiciona o diretório raiz ao path para permitir importação de 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.stripe_service import StripeService
from app.models import Company

def verify():
    print("🔍 Verificando TASK-GTM-10: SaaS Billing Engine & Metered Usage...")

    # 1. Verificar Dependência Stripe
    try:
        import stripe
        print("✅ Biblioteca 'stripe' instalada.")
    except ImportError:
        print("❌ Biblioteca 'stripe' não encontrada.")
        sys.exit(1)

    # 2. Teste de Lógica de Reporte de Uso (Mockado)
    print("🧪 Teste 1: Reporte de Uso (Metered Billing)...")
    
    mock_company = Company(
        id=uuid.uuid4(),
        name="Test Corp",
        stripe_subscription_id="sub_test_123"
    )

    # Mock da resposta do Stripe Subscription Retrieve
    mock_subscription = {
        "id": "sub_test_123",
        "items": {
            "data": [
                {
                    "id": "si_metered_123",
                    "price": {
                        "recurring": {
                            "usage_type": "metered"
                        }
                    }
                },
                {
                    "id": "si_fixed_456",
                    "price": {
                        "recurring": {
                            "usage_type": "licensed"
                        }
                    }
                }
            ]
        }
    }

    with patch("stripe.Subscription.retrieve", return_value=mock_subscription) as mock_retrieve:
        # Correção: Usar create=True para permitir mock de método dinâmico
        with patch("stripe.SubscriptionItem.create_usage_record", create=True) as mock_usage:
            
            # Executa o reporte
            StripeService.report_usage(mock_company, 500) # 500 centavos = R$ 5,00

            # Validações
            mock_retrieve.assert_called_with("sub_test_123")
            
            # Verifica se encontrou o item correto (si_metered_123)
            args, kwargs = mock_usage.call_args
            
            # O primeiro argumento posicional deve ser o ID do item
            if args[0] == "si_metered_123" and kwargs["quantity"] == 500:
                print("✅ Item metered identificado corretamente.")
                print("✅ Usage Record enviado com sucesso (Mock).")
            else:
                print(f"❌ Falha no envio do Usage Record. Args: {args}, Kwargs: {kwargs}")
                sys.exit(1)

    print("\n🏆 TASK-GTM-10: VALIDAÇÃO CONCLUÍDA.")
    sys.exit(0)

if __name__ == "__main__":
    verify()
