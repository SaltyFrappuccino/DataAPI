from aiokafka import AIOKafkaConsumer
from loguru import logger

from backend.app.config import PRODUCE_TOPIC, KAFKA_BOOTSTRAP_SERVERS


class AIOWebConsumer:
    def __init__(self, produce_topic: str = PRODUCE_TOPIC):
        self._produce_topic = produce_topic
        self._consumer = None

    async def __aenter__(self):
        if self._consumer is None:
            self._consumer = AIOKafkaConsumer(
                self._produce_topic,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
            )
            await self._consumer.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._consumer:
            await self._consumer.stop()
            self._consumer = None

    async def consumption(self):
        if self._consumer is None or self._consumer._closed:
            raise RuntimeError("Consumer is not running. Use 'async with'")
        try:
            async for msg in self._consumer:
                data_log = {
                    'topic': msg.topic,
                    'partition': msg.partition,
                    'offset': msg.offset,
                    'key': msg.key,
                    'value': msg.value.decode('utf-8') if msg.value else None,
                    'timestamp': msg.timestamp
                }
                logger.info(data_log)
                yield data_log
        except Exception as e:
            logger.error(f"Ошибка при обработке сообщений: {e}")
            raise
