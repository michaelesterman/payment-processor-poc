import logging

from models.payment import Payment
from models.payment import PaymentAssessed
from models.risk import VerdictEnum

from services.kafka_service import send_payment_to_kafka
from services.risk_assessment_service import produce_risk_assessment

logger = logging.getLogger(__name__)

async def output_payment(payment: PaymentAssessed):
    if payment.risk_assessment.verdict == VerdictEnum.ACCEPTED:
        send_payment_to_kafka(payment, 'payment_accepted_topic')
        return "SENT ACCEPTED!!!!"
    else:
        send_payment_to_kafka(payment, 'payment_declined_topic')
        return "SENT DECLINED!!!!"
    
async def process_payment(paymentJSON):
    print("PROCESSING!!!")
    
    payment = Payment.model_validate(paymentJSON)
    logger.info(payment)
        
    risk_assessment = await produce_risk_assessment(payment)
    
    payment_assessed = PaymentAssessed(payment_request=payment, risk_assessment=risk_assessment)
    logger.info(payment_assessed.model_dump_json())

    result = await output_payment(payment_assessed)

    logger.info(result)

