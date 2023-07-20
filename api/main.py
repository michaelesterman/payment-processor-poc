import json
import os
import logging
from uuid import UUID, uuid4
from enum import Enum
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Payment(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str
    userId: str = Field(..., alias='userId')
    payeeId: str = Field(..., alias='payeeId')
    paymentMethodId: str = Field(..., alias='paymentMethodId')


class StatusEnum(str, Enum):
    processing = "processing"
    success = "success"
    failure = "failure"


class PaymentResponse(BaseModel):
    status: StatusEnum
    request_id: UUID

class ErrorResponse(BaseModel):
    status: StatusEnum
    request_id: UUID
    message: str



app = FastAPI()


def get_kafka_producer():
    try:
        producer = KafkaProducer(bootstrap_servers=os.environ.get(
            'KAFKA_BROKER'), value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        return producer
    except Exception as e:
        logger.error(f"Error while creating Kafka producer: {e}")
        raise HTTPException(
            status_code=503, detail="Unable to process payment at this time")


def get_api_key(
    api_key: str = Header(None),
):
    if api_key != os.environ.get("API_KEY"):
        raise HTTPException(status_code=400, detail="Invalid API Key")
    return api_key


def convert_payment_to_dict(payment: Payment, request_id: UUID):
    try:
        payment_dict = payment.model_dump(by_alias=True)
        payment_dict['request_id'] = str(request_id)
        return payment_dict
    except Exception as e:
        logger.error(f"Error while converting payment to dict: {e}")
        raise e


def send_payment_to_kafka(payment_dict: dict):
    try:
        producer = get_kafka_producer()
        producer.send('payment_topic', payment_dict)
    except Exception as e:
        logger.error(f"Error while sending payment to Kafka: {e}")
        raise HTTPException(
            status_code=503, detail="Unable to process payment at this time")


@app.post("/payment", response_model=PaymentResponse)
async def process_payment(payment: Payment, api_key: str = Depends(get_api_key)):
    try:
        request_id = str(uuid4())

        logger.info(
            f"Processing payment: {payment.model_dump_json()}, Request ID: {request_id}")

        payment_dict = convert_payment_to_dict(payment, request_id)
        send_payment_to_kafka(payment_dict)


        return PaymentResponse(status=StatusEnum.processing, request_id=request_id)
    except HTTPException as e:
        return ErrorResponse(status=StatusEnum.failure, request_id=request_id, message=str(e.detail))