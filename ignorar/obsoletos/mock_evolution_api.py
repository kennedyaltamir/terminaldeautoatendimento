import uvicorn
from fastapi import FastAPI, Header, Body, HTTPException
from pydantic import BaseModel
import logging

# Configuração de Log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EvolutionMock")

app = FastAPI(title="Evolution API Mock", description="Simulador local para testes de WhatsApp")

class TextMessage(BaseModel):
    number: str
    options: dict
    textMessage: dict

@app.get("/instance/connectionState/{instance}")
async def check_connection_state(instance: str, apikey: str = Header(None)):
    """Simula a verificação de status da instância."""
    logger.info(f"🔍 Verificando status da instância: {instance} (Key: {apikey})")
    
    if apikey != "mock-token":
        # Simula erro de autenticação se quiser testar falhas
        # raise HTTPException(status_code=403, detail="Forbidden")
        pass

    return {
        "instance": {
            "state": "open",
            "status": "active"
        }
    }

@app.post("/message/sendText/{instance}", status_code=201)
async def send_text(instance: str, payload: TextMessage, apikey: str = Header(None)):
    """Simula o envio de mensagem de texto."""
    logger.info(f"📨 Enviando mensagem via instância: {instance}")
    logger.info(f"   Para: {payload.number}")
    logger.info(f"   Texto: {payload.textMessage['text']}")

    return {
        "key": {
            "remoteJid": f"{payload.number}@s.whatsapp.net",
            "fromMe": True,
            "id": "BAE5F8..."
        },
        "status": "PENDING",
        "message": {
            "conversation": payload.textMessage['text']
        }
    }

if __name__ == "__main__":
    print("🤖 Iniciando Mock da Evolution API na porta 8001...")
    print("👉 Configure seu .env com:")
    print('   WHATSAPP_API_URL=http://localhost:8001')
    print('   WHATSAPP_INSTANCE=mock-instance')
    print('   WHATSAPP_API_TOKEN=mock-token')
    print("---------------------------------------------------")
    uvicorn.run(app, host="0.0.0.0", port=8001)
