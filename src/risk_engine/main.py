import asyncio
from enum import Enum
import logging
from concurrent.futures import ThreadPoolExecutor
import random
from services.kafka_service import get_kafka_consumer
from models.payment import Payment
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

executor = ThreadPoolExecutor(max_workers=5)

class VerdictEnum(str, Enum):
    ACCEPTED = "accepted"
    DECLINED = "declined"

class RiskAssessment(BaseModel):
    payment_id: str
    risk_level: float
    verdict: VerdictEnum

class PaymentAssessed(BaseModel):
     payment_request: Payment
     risk_assessment: RiskAssessment

async def output_payment(payment):
    print("")
    
async def produce_risk_assessment(payment: Payment):
    rand_num = random.uniform(0, 1)
    if rand_num <= 0.7:
        return RiskAssessment(payment_id=payment.payment_id, risk_level=rand_num, verdict=VerdictEnum.ACCEPTED)
    else:
        return RiskAssessment(payment_id=payment.payment_id, risk_level=rand_num, verdict=VerdictEnum.DECLINED)

async def consume_message(consumer):
    for message in consumer:
        payment = Payment.model_validate(message.value)
        logger.info(payment)
        
        risk_assessment = await produce_risk_assessment(payment)
        payment_assessed = PaymentAssessed(payment_request=payment, risk_assessment=risk_assessment)

        logger.info(payment_assessed.model_dump_json())

        
def main():
    logger.info("Risk engine startup")
    try:
        consumer = get_kafka_consumer("payment_topic")

        loop = asyncio.get_event_loop()

        loop.run_until_complete(consume_message(consumer))
    except Exception as e:
        logger.error(f"Unexpected error while doing risk assessment: {str(e)}")

main()