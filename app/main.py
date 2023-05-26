import os

from fastapi import FastAPI
from dotenv import load_dotenv

from app.Core.Kafka import Kafka

load_dotenv(verbose=True)
app = FastAPI()

GAME_SERVICE_TOPIC = os.environ.get("GAME_SERVICE_TOPIC")

KafkaInstance = None

@app.get("/")
async def root():
    await KafkaInstance.produce(GAME_SERVICE_TOPIC, "Hello World")

@app.on_event("startup")
async def startup_event():
    global KafkaInstance
    KafkaInstance = Kafka()
    await KafkaInstance.init()

@app.on_event("shutdown")
async def shutdown_event():
    await KafkaInstance.close()

