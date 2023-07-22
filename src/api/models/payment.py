from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from enums.status_enum import StatusEnum


class Payment(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str
    user_id: str = Field(..., alias='userId')
    payee_id: str = Field(..., alias='payeeId')
    payment_method_id: str = Field(..., alias='paymentMethodId')
    payment_id: str = Field(default_factory=lambda: str(uuid4()))

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