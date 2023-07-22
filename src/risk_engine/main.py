import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

from services.payment_processing_service import process_payment
from services.kafka_service import get_kafka_consumer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

executor = ThreadPoolExecutor(max_workers=5)


async def process_queue(consumer):
    for message in consumer:
        await process_payment(message.value)

        
def main():
    logger.info("Risk engine startup")
    try:
        consumer = get_kafka_consumer("payment_topic")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(process_queue(consumer))
    except Exception as e:
        logger.error(f"Unexpected error while doing risk assessment: {str(e)}")

main()