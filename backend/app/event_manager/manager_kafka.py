from backend.app.event_manager.consumer import AIOWebConsumer
from backend.app.event_manager.producer import AIOWebProducer


class ManagerKafka:

    def __init__(self):
        self._producer = None
        self._consumer = None

    @property
    def consumer(self) -> AIOWebConsumer:
        if self._consumer is None:
            self._consumer = AIOWebConsumer()
        return self._consumer

    @property
    def producer(self):
        return AIOWebProducer()
