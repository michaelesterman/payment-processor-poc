from pydantic import BaseModel, Field
from models.risk import RiskAssessment


class Payment(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str
    user_id: str = Field(..., alias='user_id')
    payee_id: str = Field(..., alias='payee_id')
    payment_method_id: str = Field(..., alias='payment_method_id')
    payment_id: str = Field(..., alias='payment_id')

class PaymentAssessed(BaseModel):
     payment_request: Payment
     risk_assessment: RiskAssessment

