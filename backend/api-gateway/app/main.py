from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import user_routes, stock_routes, websocket_routes
from app.config import RABBITMQ_URL
from app.messaging.consumer import (
    start_stock_consumer,
    stop_stock_consumer,
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Khi API Gateway khởi động
    await start_stock_consumer(RABBITMQ_URL)

    yield

    # Khi API Gateway tắt
    await stop_stock_consumer()


app = FastAPI(
    title="Stock Management API Gateway",
    description="API Gateway for Microservices",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_routes.router)
app.include_router(stock_routes.router)
app.include_router(websocket_routes.router)


@app.get("/")
async def root():
    return {"message": "API Gateway is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
