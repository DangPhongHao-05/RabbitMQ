from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import connect_to_mongodb, close_mongodb_connection, get_database

from app.messaging.rabbitmq import connect_rabbitmq, start_user_consumer, close_rabbitmq

from app.routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Kết nối MongoDB
    await connect_to_mongodb()
    app.state.db = get_database()

    # Kết nối RabbitMQ
    await connect_rabbitmq()

    # Bắt đầu nhận message
    await start_user_consumer()

    print("User Service is ready!")

    yield

    # Đóng kết nối
    await close_rabbitmq()
    await close_mongodb_connection()


app = FastAPI(
    title="User Service",
    description="Microservice quản lý người dùng",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth.router)


@app.get("/")
async def home():
    return {"message": "User Service is running"}


@app.get("/health/db")
async def check_database():
    db = app.state.db

    collections = await db.list_collection_names()

    return {"database": db.name, "status": "connected", "collections": collections}
