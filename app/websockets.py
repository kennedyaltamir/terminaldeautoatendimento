import os
import json
import asyncio
import logging
from typing import List, Dict
from fastapi import WebSocket
import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("WebSocketManager")

class RedisConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis_client: redis.Redis | None = None
        self.pubsub = None
        self.reader_task = None
        self.use_redis = False # Flag de controle

    async def startup(self):
        """Inicializa conexão com Redis e Worker de leitura"""
        try:
            # Tenta conectar com timeout curto para não travar o boot
            self.redis_client = redis.from_url(
                self.redis_url, 
                encoding="utf-8", 
                decode_responses=True,
                socket_connect_timeout=2 # 2 segundos de timeout
            )
            await self.redis_client.ping()
            
            self.pubsub = self.redis_client.pubsub()
            self.reader_task = asyncio.create_task(self._redis_reader())
            self.use_redis = True
            logger.info(f"🔌 Redis Pub/Sub conectado em {self.redis_url}")
        except Exception as e:
            logger.warning(f"⚠️ Redis indisponível ({e}). Usando modo memória local (sem escala).")
            self.use_redis = False
            self.redis_client = None

    async def shutdown(self):
        """Fecha conexões graciosamente"""
        if self.reader_task:
            self.reader_task.cancel()
        if self.pubsub:
            await self.pubsub.close()
        if self.redis_client:
            await self.redis_client.close()
        logger.info("🔌 Redis Pub/Sub desconectado")

    async def connect(self, websocket: WebSocket, company_slug: str):
        await websocket.accept()
        
        if company_slug not in self.active_connections:
            self.active_connections[company_slug] = []
            
            # Só tenta assinar se o Redis estiver ativo
            if self.use_redis and self.pubsub:
                try:
                    await self.pubsub.subscribe(f"mesaflow:{company_slug}")
                    logger.debug(f"📡 Assinado canal Redis: mesaflow:{company_slug}")
                except Exception as e:
                    logger.error(f"❌ Erro ao assinar Redis: {e}")
                    self.use_redis = False # Desativa Redis se falhar no meio do caminho

        self.active_connections[company_slug].append(websocket)
        logger.info(f"➕ Nova conexão WS local: {company_slug}. Total: {len(self.active_connections[company_slug])}")

    def disconnect(self, websocket: WebSocket, company_slug: str):
        if company_slug in self.active_connections:
            if websocket in self.active_connections[company_slug]:
                self.active_connections[company_slug].remove(websocket)
            
            if not self.active_connections[company_slug]:
                del self.active_connections[company_slug]
                
    async def broadcast(self, message: dict, company_slug: str):
        """
        Publica a mensagem no Redis (se disponível) ou envia localmente.
        """
        if self.use_redis and self.redis_client:
            channel = f"mesaflow:{company_slug}"
            try:
                await self.redis_client.publish(channel, json.dumps(message))
            except Exception as e:
                logger.error(f"❌ Erro ao publicar no Redis: {e}. Fallback para local.")
                self.use_redis = False
                await self._local_broadcast(message, company_slug)
        else:
            # Fallback para memória local
            await self._local_broadcast(message, company_slug)

    async def _local_broadcast(self, message: dict, company_slug: str):
        """Envia para conexões locais (Fallback ou chamado pelo Reader)"""
        if company_slug in self.active_connections:
            # Copia a lista para evitar erro de modificação durante iteração
            connections = self.active_connections[company_slug][:]
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception:
                    self.disconnect(connection, company_slug)

    async def _redis_reader(self):
        """Loop infinito que escuta o Redis e despacha para WebSockets locais"""
        if not self.pubsub:
            return

        try:
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    channel = message["channel"]
                    if ":" in channel:
                        slug = channel.split(":", 1)[1]
                        try:
                            data = json.loads(message["data"])
                            await self._local_broadcast(data, slug)
                        except json.JSONDecodeError:
                            logger.error("Erro ao decodificar JSON do Redis")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"❌ Erro fatal no Redis Reader: {e}")
            self.use_redis = False

manager = RedisConnectionManager()