from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from enums.status_enum import StatusEnum


class Payment(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str
    userId: str = Field(..., alias='userId')
    payeeId: str = Field(..., alias='payeeId')
    paymentMethodId: str = Field(..., alias='paymentMethodId')

class PaymentResponse(BaseModel):
    status: StatusEnum
    payment_id: str
    message: Optional[str] = None

def convert_payment_to_dict(payment: Payment, payment_id: UUID):
    try:
        payment_dict = payment.model_dump(by_alias=True)
        payment_dict['payment_id'] = str(payment_id)
        return payment_dict
    except Exception as e:
        raise Exception("Error while converting payment to dict")