import json
import aio_pika

from app.config import settings


async def main():
    # Kết nối RabbitMQ
    connection = await aio_pika.connect_robust(settings.rabbitmq_url)

    channel = await connection.channel()

    # Khai báo Exchange
    exchange = await channel.declare_exchange(
        "stock.events", aio_pika.ExchangeType.TOPIC, durable=True
    )

    # Dữ liệu sự kiện
    event_data = {
        "event": "stock.created",
        "data": {"code": "FPT", "name": "FPT Corporation", "price": 100},
    }

    # Gửi sự kiện
    await exchange.publish(
        aio_pika.Message(
            body=json.dumps(event_data).encode(), content_type="application/json"
        ),
        routing_key="stock.created",
    )

    print("Đã gửi sự kiện stock.created!")

    await connection.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
