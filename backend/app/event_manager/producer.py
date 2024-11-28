from aiokafka import AIOKafkaProducer
from loguru import logger

from backend.app.config import KAFKA_BOOTSTRAP_SERVERS, PRODUCE_TOPIC


class AIOWebProducer:
    def __init__(self, produce_topic: str = PRODUCE_TOPIC):
        self._producer = None
        self._produce_topic = produce_topic

    async def __aenter__(self):
        if self._producer is None:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
            )
            await self._producer.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._producer:
            await self._producer.stop()
            self._producer = None

    async def send(self, value: bytes):
        if self._producer is None or self._producer._closed:
            raise RuntimeError("Producer is not running. Use 'async with' or call 'start' first.")
        try:
            await self._producer.send(
                topic=self._produce_topic,
                value=value,
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")
            raise
