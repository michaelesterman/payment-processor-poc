import logging
from uuid import uuid4
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from services.kafka_service import send_payment_to_kafka
from services.auth_service import get_api_key
from enums.status_enum import StatusEnum
from models.payment import Payment, PaymentResponse, convert_payment_to_dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/payment")
async def process_payment(payment: Payment, api_key: str = Depends(get_api_key)):
    try:        
        logger.info(
            f"Processing payment: {payment.model_dump_json()}, Request ID: {payment.payment_id}")
        
        await send_payment_to_kafka(payment)

        return JSONResponse(status_code=200, content=PaymentResponse(status=StatusEnum.processing, payment_id=payment.payment_id).model_dump())
    except Exception as e:
        logger.error(f"Unexpected error while processing payment: {str(e)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=PaymentResponse(status=StatusEnum.failure, payment_id=payment.payment_id, message="Unexpected error while processing payment").model_dump())
