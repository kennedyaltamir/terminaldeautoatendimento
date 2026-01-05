import os
import json
import logging
import redis.asyncio as redis
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from pathlib import Path

load_dotenv() # Carrega variáveis de ambiente

logger = logging.getLogger("WebSocketManager")

class RedisConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis_client: redis.Redis | None = None
        self.pubsub = None
        self.reader_task = None
        self.use_redis = False # Flag para controlar se o Redis está ativo

    async def startup(self):
        """Inicializa conexão com Redis e o worker de leitura do Pub/Sub."""
        try:
            # Tenta conectar com timeout curto para não travar o boot
            self.redis_client = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=2 # Timeout curto para verificação inicial
            )
            await self.redis_client.ping() # Verifica a conexão
            self.pubsub = self.redis_client.pubsub()
            # Cria a task de leitura do Redis em background
            self.reader_task = asyncio.create_task(self._redis_reader())
            self.use_redis = True
            logger.info(f"🚀 Redis Pub/Sub conectado em {self.redis_url}")
        except Exception as e:
            logger.warning(f"⚠️ Redis indisponível ({e}). Usando modo memória local (sem escala para broadcast).")
            self.use_redis = False
            self.redis_client = None

    async def shutdown(self):
        """Fecha conexões com Redis graciosamente."""
        if self.reader_task:
            self.reader_task.cancel() # Cancela a tarefa de leitura
        if self.pubsub:
            try: await self.pubsub.close() # Fecha a conexão PubSub
            except Exception as e: logger.error(f"Erro ao fechar PubSub: {e}")
        if self.redis_client:
            try: await self.redis_client.close() # Fecha a conexão principal do Redis
            except Exception as e: logger.error(f"Erro ao fechar Redis client: {e}")
        logger.info("🔌 Redis Pub/Sub desconectado")

    async def connect(self, websocket: WebSocket, company_slug: str):
        """Registra nova conexão WebSocket e assina o canal Redis correspondente."""
        await websocket.accept() # Aceita a conexão do cliente

        # Cria a lista de conexões para o tenant se ela não existir
        if company_slug not in self.active_connections:
            self.active_connections[company_slug] = []
            
            # Assina o canal do tenant no Redis apenas se o serviço estiver ativo
            if self.use_redis and self.pubsub:
                channel = f"mesaflow:{company_slug}"
                try:
                    await self.pubsub.subscribe(channel)
                    logger.debug(f"📡 Assinado canal Redis: {channel}")
                except Exception as e:
                    logger.error(f"❌ Falha ao assinar canal Redis '{channel}': {e}. Desativando Redis.")
                    self.use_redis = False # Desativa o Redis se a assinatura falhar

        # Adiciona a conexão à lista do tenant
        self.active_connections[company_slug].append(websocket)
        logger.info(f"➕ Nova conexão WS: {company_slug} ({len(self.active_connections[company_slug])} total)")

    def disconnect(self, websocket: WebSocket, company_slug: str):
        """Remove uma conexão WebSocket inativa da lista do tenant."""
        if company_slug in self.active_connections:
            try:
                self.active_connections[company_slug].remove(websocket)
                # Se não houver mais conexões ativas para este tenant
                if not self.active_connections[company_slug]:
                    del self.active_connections[company_slug] # Remove o tenant da lista
                    # Se o Redis estiver ativo e o canal existir, desassina
                    if self.use_redis and self.pubsub and company_slug not in self.active_connections:
                         try:
                             # Desassina em background para não bloquear a thread principal
                             asyncio.create_task(self.pubsub.unsubscribe(f"mesaflow:{company_slug}"))
                             logger.debug(f"📡 Desassinado canal Redis: mesaflow:{company_slug}")
                         except Exception as e:
                             logger.error(f"Erro ao desassinar canal Redis: {e}")
            except ValueError:
                # O WebSocket pode já ter sido removido, ignora o erro
                pass
            logger.info(f"➖ Conexão WS removida: {company_slug} ({len(self.active_connections.get(company_slug, []))} restantes)")

    async def broadcast(self, message: dict, company_slug: str):
        """
        Publica a mensagem no Redis (se ativo) ou envia diretamente às conexões locais.
        Garante que dados complexos (como Decimal, datetime) sejam serializados.
        """
        if self.use_redis and self.redis_client:
            channel = f"mesaflow:{company_slug}"
            try:
                # Usa json.dumps com default=str para serializar tipos não nativos
                await self.redis_client.publish(channel, json.dumps(message, default=str))
            except Exception as e:
                logger.error(f"❌ Erro ao publicar no Redis ({channel}): {e}. Fallback para broadcast local.")
                self.use_redis = False # Desativa Redis se a publicação falhar
                await self._local_broadcast(message, company_slug)
        else:
            # Envia diretamente para conexões locais se Redis não estiver ativo ou falhar
            await self._local_broadcast(message, company_slug)

    async def _local_broadcast(self, message: dict, company_slug: str):
        """Envia a mensagem para todas as conexões WebSocket conectadas para o tenant."""
        if company_slug in self.active_connections:
            # Cria uma cópia da lista de conexões para evitar erro se uma conexão for fechada durante o loop
            connections = list(self.active_connections[company_slug])
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Erro ao enviar WS para {company_slug}: {e}")
                    # Remove a conexão inválida da lista
                    self.disconnect(connection, company_slug)

    async def _redis_reader(self):
        """Loop assíncrono que escuta mensagens do Redis Pub/Sub e as repassa."""
        if not self.pubsub:
            return
            
        subscribed_channels = set() # Mantém controle dos canais assinados
        try:
            # Na inicialização, tenta assinar todos os canais relevantes que podem já existir
            if self.use_redis and self.redis_client:
                active_keys = await self.redis_client.keys("mesaflow:*")
                for key in active_keys:
                    if key.startswith("mesaflow:"):
                        slug = key.split(":", 1)
                        if slug and slug not in subscribed_channels:
                            await self.pubsub.subscribe(key)
                            subscribed_channels.add(slug)
                            logger.debug(f"📡 Assinado canal Redis inicial: {key}")

            # Loop principal de escuta de mensagens
            async for message in self.pubsub.listen():
                if message['type'] == 'subscribe':
                    # Ignora confirmações de subscrição
                    continue
                elif message['type'] == 'message':
                    channel = message['channel']
                    if channel.startswith('mesaflow:'):
                        slug = channel.split(':', 1) # Pega o slug do canal
                        try:
                            data = json.loads(message['data'])
                            # Repassa a mensagem apenas se houver conexões ativas para o slug
                            if slug in self.active_connections:
                                await self._local_broadcast(data, slug)
                        except json.JSONDecodeError:
                            logger.error("Erro ao decodificar JSON recebido do Redis Pub/Sub.")
                        except Exception as e:
                            logger.error(f"Erro ao processar mensagem Redis Pub/Sub ({channel}): {e}")
                elif message['type'] == 'psubscribe':
                     # Ignora confirmações de psubscribe
                     pass
                else:
                    logger.warning(f"Recebido tipo de mensagem Redis desconhecido: {message['type']}")

        except asyncio.CancelledError:
            logger.info("Task do Redis Reader cancelada.") # Gracefully shutdown
        except Exception as e:
            logger.critical(f"❌ Erro fatal no loop do Redis Reader: {e}. Desativando Redis.")
            self.use_redis = False # Desativa o Redis se ocorrer um erro crítico
        finally:
            logger.info("Loop do Redis Reader encerrado.")

# Instância global do gerenciador de conexões WebSocket
manager = RedisConnectionManager()

# Exemplo de como integrar este manager no app FastAPI (em app/main.py):
#
# @app.on_event("startup")
# async def startup_event():
#     await manager.startup()
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     await manager.shutdown()
#
# @app.websocket("/ws/{company_slug}")
# async def websocket_endpoint(websocket: WebSocket, company_slug: str):
#     await manager.connect(websocket, company_slug)
#     try:
#         while True:
#             # Exemplo: pode esperar por mensagens do cliente (ex: localização do entregador)
#             # data = await websocket.receive_json()
#             # if data.get("type") == "driver_location":
#             #     await manager.broadcast(data, company_slug) # Retransmite para outros clientes
#             await asyncio.sleep(1) # Manter conexão viva
#     except WebSocketDisconnect:
#         manager.disconnect(websocket, company_slug)
#     except Exception as e:
#         logger.error(f"Erro no WebSocket ({company_slug}): {e}")
#         manager.disconnect(websocket, company_slug)
