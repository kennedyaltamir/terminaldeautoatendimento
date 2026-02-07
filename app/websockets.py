# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-26 05:55:00
# DESCRIPTION: WebSocket Manager com correção de typo no log de fallback.
import os
import json
import logging
import redis.asyncio as redis
import asyncio
from fastapi import WebSocket
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("WebSocketManager")

class RedisConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis_client: Optional[redis.Redis] = None
        self.pubsub = None
        self.reader_task = None
        self.use_redis = False

    async def startup(self):
        try:
            self.redis_client = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=2
            )
            await self.redis_client.ping()
            self.pubsub = self.redis_client.pubsub()
            self.reader_task = asyncio.create_task(self._redis_reader())
            self.use_redis = True
            logger.info(f"🚀 Redis Pub/Sub conectado em {self.redis_url}")
        except Exception as e:
            # FIX: Typo "broadcastt" corrigido para "broadcast"
            logger.warning(f"⚠️ Redis indisponível ({e}). Usando modo memória local (sem escala para broadcast).")
            self.use_redis = False
            self.redis_client = None

    async def shutdown(self):
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
            if self.use_redis and self.pubsub:
                channel = f"mesaflow:{company_slug}"
                await self.pubsub.subscribe(channel)
        self.active_connections[company_slug].append(websocket)
        logger.info(f"➕ Nova conexão WS: {company_slug} ({len(self.active_connections[company_slug])} total)")

    def disconnect(self, websocket: WebSocket, company_slug: str):
        if company_slug in self.active_connections:
            try:
                self.active_connections[company_slug].remove(websocket)
                if not self.active_connections[company_slug]:
                    del self.active_connections[company_slug]
            except ValueError:
                pass

    async def broadcast(self, message: dict, company_slug: str):
        if self.use_redis and self.redis_client:
            channel = f"mesaflow:{company_slug}"
            try:
                await self.redis_client.publish(channel, json.dumps(message, default=str))
            except Exception:
                await self._local_broadcast(message, company_slug)
        else:
            await self._local_broadcast(message, company_slug)

    async def _local_broadcast(self, message: dict, company_slug: str):
        if company_slug in self.active_connections:
            for connection in list(self.active_connections[company_slug]):
                try:
                    await connection.send_json(message)
                except Exception:
                    self.disconnect(connection, company_slug)

    async def _redis_reader(self):
        if not self.pubsub:
            return
        try:
            async for message in self.pubsub.listen():
                if message['type'] == 'message':
                    channel = message['channel']
                    slug = channel.split(':', 1)[1]
                    data = json.loads(message['data'])
                    await self._local_broadcast(data, slug)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.critical(f"❌ Erro fatal no Redis Reader: {e}")
            self.use_redis = False

manager = RedisConnectionManager()
