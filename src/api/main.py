from fastapi import FastAPI
from routes import payment_route

app = FastAPI()

app.include_router(payment_route.router)
