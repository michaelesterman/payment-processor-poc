import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from services.kafka_service import get_kafka_consumer
from services.risk_assessment_service import assign_risk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

executor = ThreadPoolExecutor(max_workers=5)

async def consume_message(consumer):
    for message in consumer:
        logger.info(message)
        await asyncio.sleep(1)  # simulate I/O-bound work with asyncio.sleep

def main():
    logger.info("Risk engine startup")
    try:
        consumer = get_kafka_consumer("payment_topic")

        loop = asyncio.get_event_loop()

        loop.run_until_complete(consume_message(consumer))
    except Exception as e:
        logger.error(f"Unexpected error while doing risk assessment: {str(e)}")

main()