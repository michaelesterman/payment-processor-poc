uvicorn main:app --reload



curl --location 'http://127.0.0.1:8000/payment' \
--header 'API-KEY: MY-API-KEY' \
--header 'Content-Type: application/json' \
--data '{
    "amount": 70.5,
    "currency": "USD",
    "userId": "user123",
    "payeeId": "payee123",
    "paymentMethodId": "method123"
}'
