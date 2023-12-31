import json
import os
import time
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

from models.payment import PaymentAssessed



def get_kafka_producer():
    try:
        producer = KafkaProducer(bootstrap_servers=os.environ.get(
            'KAFKA_BROKER'), value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        return producer
    except Exception as e:
        raise Exception(f"Error while creating Kafka producer: {e}")


def get_kafka_consumer(topic: str):
    while True:
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=os.environ.get('KAFKA_BROKER'),
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                enable_auto_commit=True,
                auto_offset_reset='earliest',
                group_id="risk_engines")
            return consumer
        except NoBrokersAvailable:
            wait_time = 2  # wait time in seconds
            print(f"Kafka is not available, retrying in {wait_time} seconds.")
            time.sleep(wait_time)
            continue
        except Exception as e:
            raise Exception(f"Error while creating Kafka consumer: {e}")


def send_payment_to_kafka(payment: PaymentAssessed, topic: str):
    try:
        producer = get_kafka_producer()
        producer.send(topic, payment.model_dump())
    except Exception as e:
        raise Exception(f"Error while sending accepted payment to Kafka: {e}")

