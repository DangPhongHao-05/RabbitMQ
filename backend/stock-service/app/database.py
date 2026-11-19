from pymongo import AsyncMongoClient

from app.config import settings

client = None
database = None


async def connect_to_mongodb():
    global client, database

    client = AsyncMongoClient(settings.mongodb_url)

    await client.admin.command("ping")

    database = client[settings.database_name]

    print("Stock Service connected to MongoDB!")


async def close_mongodb_connection():
    global client

    if client is not None:
        await client.close()
        print("MongoDB connection closed!")


def get_database():
    return database
