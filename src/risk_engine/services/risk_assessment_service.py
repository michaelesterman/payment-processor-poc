import random

from models.payment import Payment
from models.risk import RiskAssessment, VerdictEnum


async def produce_risk_assessment(payment: Payment):
    rand_num = random.uniform(0, 1)
    if rand_num <= 0.7:
        return RiskAssessment(payment_id=payment.payment_id, risk_level=rand_num, verdict=VerdictEnum.ACCEPTED)
    else:
        return RiskAssessment(payment_id=payment.payment_id, risk_level=rand_num, verdict=VerdictEnum.DECLINED)