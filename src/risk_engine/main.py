from fastapi import FastAPI
import logging
from services.kafka_service import get_kafka_consumer
from services.risk_assessment_service import assign_risk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def main():
    logger.info("Application startup")
    try:
        consumer = get_kafka_consumer("payment_topic")

        for message in consumer:
            logger.info(message)
    except Exception as e:
        logger.error(f"Unexpected error while doing risk assessment: {str(e)}")

main()