import asyncio
import aio_pika

from app.config import settings
from urllib.parse import urlsplit


async def main():
    url = urlsplit(settings.rabbitmq_url)

    print("Connecting to:", url.hostname, url.port)
    print("Username:", url.username)

    try:
        connection = await aio_pika.connect_robust(settings.rabbitmq_url)

        print("RabbitMQ connection successful!")

        await connection.close()

    except Exception as e:
        print("Connection failed:", repr(e))


asyncio.run(main())
