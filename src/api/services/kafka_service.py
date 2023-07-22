import json
import os
import time
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from models.payment import Payment

async def get_kafka_producer():
    while True:
        try:
            producer = KafkaProducer(bootstrap_servers=os.environ.get(
                'KAFKA_BROKER'), value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            return producer
        except NoBrokersAvailable:
                wait_time = 1  # wait time in seconds
                print(f"Kafka is not available, retrying in {wait_time} seconds.")
                time.sleep(wait_time)
                continue
        except Exception as e:
            raise Exception(f"Error while creating Kafka producer: {e}")
    
async def send_payment_to_kafka(payment: Payment):
    try:
        producer = await get_kafka_producer()
        producer.send('payment_topic', payment.model_dump())
    except Exception as e:
        raise Exception(f"Error while sending payment to Kafka: {e}")