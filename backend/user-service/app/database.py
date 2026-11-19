from pymongo import AsyncMongoClient
from app.config import settings

client = None
database = None


async def connect_to_mongodb():
    global client, database

    # Khởi tạo kết nối MongoDB
    client = AsyncMongoClient(settings.mongodb_url)

    # Kiểm tra kết nối
    await client.admin.command("ping")

    # Chọn database
    database = client[settings.database_name]

    print("Connected to MongoDB successfully!")


async def close_mongodb_connection():
    global client

    if client is not None:
        await client.close()
        print("MongoDB connection closed!")


def get_database():
    return database
