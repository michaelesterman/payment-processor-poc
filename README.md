# Quickstart

## Installation

```sh
docker compose up
```

## Testing

### Sending a payment

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


### Listing topics

```sh
docker exec -it kafka kafka-topics.sh --list --bootstrap-server localhost:9092
```

### Peeking messages

#### Accepted:

```sh
docker exec -it kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic payment_accepted_topic --from-beginning
```

#### Declined:

```sh
docker exec -it kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic payment_accepted_topic --from-beginning
```

# Development

## Logs

docker compose logs -f api
docker compose logs -f risk_engine


## Making changes to the container

### Rebuild specific Docker image

```sh
docker compose build api
```

### Restart the service

```sh
docker compose up -d api
```

# Database

## Schema

The database structure for storing these data can be split into two tables: `payments` and `risk_assessments`. Here is a simple suggestion:

`payments` table:

- `payment_id` (`UUID`): Primary key, unique identifier for each payment.
- `amount` (`NUMERIC`): Amount of the payment.
- `currency` (`CHAR(3)`): Currency of the payment.
- `user_id` (`UUID`): Identifier of the user who made the payment.
- `payee_id` (`UUID`): Identifier of the payee who receives the payment.
- `payment_method_id` (`UUID`): Identifier of the payment method used.

`risk_assessments` table:

- `assessment_id` (`UUID`): Primary key, unique identifier for each risk assessment.
- `payment_id` (`UUID`): Foreign key, links to the payment_id in the payments table.
- `risk_level` (`DOUBLE PRECISION`): Risk level of the payment.
- `verdict` (`ENUM`): Verdict of the risk assessment (Accepted or Declined).

The two tables are linked through a one-to-one relationship by the `payment_id` field.