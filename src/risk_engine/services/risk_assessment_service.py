import random

from models.payment import Payment, PaymentAssessed


def assign_risk(payment: Payment) -> PaymentAssessed:
    risk = random.uniform(0, 1)
    return {**payment, 'risk': risk}