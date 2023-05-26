import os

import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from dotenv import load_dotenv

load_dotenv(verbose=True)

KAFKA_SERVER_URL = os.environ.get("BOOTSTRAP_SERVERS")
KAFKA_SERVICE_TOPIC = os.environ.get("SERVICE_TOPIC")

print("KAFKA_SERVER_URL: "+KAFKA_SERVER_URL)
print("KAFKA_SERVICE_TOPIC: "+KAFKA_SERVICE_TOPIC)

class Kafka:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.consumer = AIOKafkaConsumer(KAFKA_SERVICE_TOPIC, loop=self.loop, bootstrap_servers=KAFKA_SERVER_URL)
        self.producer = AIOKafkaProducer(loop=self.loop, bootstrap_servers=KAFKA_SERVER_URL)

    async def init(self):
        await self.producer.start()
        await self.consumer.start()

        self.loop.create_task(self.consume())

    async def consume(self):
        try:
            async for msg in self.consumer:
                print(
                    "consumed: ",
                    msg.topic,
                    msg.partition,
                    msg.offset,
                    msg.key,
                    msg.value,
                    msg.timestamp,
                )
        finally:
            await self.consumer.stop()

    async def produce(self, topic, message: str):
        try:
            await self.producer.send(topic, b"Hello World")
        except Exception:
            print("Error sending the message to the kafka queue")

    async def close(self):
        await self.producer.stop()
        await self.consumer.stop()
