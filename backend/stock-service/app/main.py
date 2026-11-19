from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routers import stock
from app.database import (
    connect_to_mongodb,
    close_mongodb_connection,
    get_database,
)
from app.messaging.rabbitmq import (
    connect_rabbitmq,
    close_rabbitmq,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Kết nối MongoDB
    await connect_to_mongodb()
    app.state.db = get_database()

    # Kết nối RabbitMQ
    await connect_rabbitmq()

    print("Stock Service is ready!")

    yield

    # Đóng kết nối khi service dừng
    await close_rabbitmq()
    await close_mongodb_connection()


app = FastAPI(
    title="Stock Service",
    description="Microservice quản lý cổ phiếu",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(stock.router)


@app.get("/")
async def home():
    return {"message": "Stock Service is running"}


@app.get("/health/db")
async def check_database():
    db = app.state.db
    collections = await db.list_collection_names()

    return {
        "database": db.name,
        "status": "connected",
        "collections": collections,
    }
