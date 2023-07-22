import json
import os
from kafka import KafkaProducer

from models.payment import Payment

async def get_kafka_producer():
    try:
        producer = KafkaProducer(bootstrap_servers=os.environ.get(
            'KAFKA_BROKER'), value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        return producer
    except Exception as e:
        raise Exception(f"Error while creating Kafka producer: {e}")
    
async def send_payment_to_kafka(payment: Payment):
    try:
        producer = await get_kafka_producer()
        producer.send('payment_topic', payment.model_dump())
    except Exception as e:
        raise Exception(f"Error while sending payment to Kafka: {e}")