from pydantic import BaseModel, Field
from models.risk import RiskAssessment


class Payment(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str
    userId: str = Field(..., alias='userId')
    payeeId: str = Field(..., alias='payeeId')
    paymentMethodId: str = Field(..., alias='paymentMethodId')
    payment_id: str = Field(..., alias='payment_id')

class PaymentAssessed(BaseModel):
     payment_request: Payment
     risk_assessment: RiskAssessment

