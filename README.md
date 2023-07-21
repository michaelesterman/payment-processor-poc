# Quickstart

## Installation

```sh
docker compose up
```

## Testing

```sh
curl --location 'http://127.0.0.1:8000/payment' \
--header 'API-KEY: MY-API-KEY' \
--header 'Content-Type: application/json' \
--data '{
    "amount": 70.5,
    "currency": "USD",
    "userId": "73ff3a2e-379c-4b89-8e2a-2c84ba2f7378",
    "payeeId": "844b3baa-c18b-4076-b660-96dfd1120de9",
    "paymentMethodId": "5afe0d8f-53df-48b1-a813-fa2d58e54f78"
}'
```

# Kafka

## Listing topics

```sh
docker exec -it payment-processor-poc-kafka-1 kafka-topics.sh --list --bootstrap-server localhost:9092
```

## Peeking messages

```sh
docker exec -it kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic payment_topic --from-beginning
```

# Development

## Logs

docker compose logs -f api
docker compose logs -f risk_engine


## Making changes to the container

### Rebuild the Docker image

```sh
docker compose build api
```

### Restart the service

```sh
docker compose up -d api
```

## Running the API locally

From `src/api`:


```sh
uvicorn main:app --reload
```
