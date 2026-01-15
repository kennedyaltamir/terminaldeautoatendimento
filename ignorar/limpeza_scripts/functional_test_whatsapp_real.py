import asyncio
import os
import sys
from dotenv import load_dotenv

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.whatsapp_service import WhatsAppService
from app.models import Company

# Carrega variáveis de ambiente
load_dotenv()

async def test_real_whatsapp():
    print("📱 Teste de Integração Real: WhatsApp (Evolution API)")
    print("---------------------------------------------------")

    api_url = os.getenv("WHATSAPP_API_URL")
    instance = os.getenv("WHATSAPP_INSTANCE")
    token = os.getenv("WHATSAPP_API_TOKEN")

    if not api_url or not instance or not token:
        print("❌ Configurações de WhatsApp não encontradas no .env")
        print("   Defina: WHATSAPP_API_URL, WHATSAPP_INSTANCE, WHATSAPP_API_TOKEN")
        return

    print(f"📡 API URL: {api_url}")
    print(f"🆔 Instância: {instance}")

    service = WhatsAppService()
    
    # Mock de objeto Company com as configs do .env
    # Isso simula uma empresa que não tem config própria e usa a global
    mock_company = Company(
        whatsapp_api_url=None, 
        whatsapp_instance=None, 
        whatsapp_token=None
    )

    # 1. Verificar Status
    print("\n🔍 Verificando status da instância...")
    status = await service.get_instance_status(mock_company)
    print(f"   Status: {status}")

    if status.get("status") != "open":
        print("⚠️  A instância não parece estar conectada (open). O envio pode falhar.")
        proceed = input("   Deseja tentar enviar mesmo assim? (s/n): ")
        if proceed.lower() != 's':
            return

    # 2. Enviar Mensagem
    target_phone = input("\n📱 Digite o número de destino (com DDD, ex: 11999999999): ").strip()
    if not target_phone:
        print("❌ Número inválido.")
        return

    print(f"📤 Enviando mensagem de teste para {target_phone}...")
    
    # Usamos o método privado _send_http_request diretamente para testar o envio bruto
    # ou usamos send_test_message se configurarmos o whatsapp_number no mock
    mock_company.whatsapp_number = target_phone
    
    success = await service.send_test_message(mock_company)

    if success:
        print("✅ Mensagem enviada com sucesso! Verifique o celular.")
    else:
        print("❌ Falha ao enviar mensagem. Verifique os logs.")

if __name__ == "__main__":
    try:
        asyncio.run(test_real_whatsapp())
    except KeyboardInterrupt:
        print("\nCancelado.")
