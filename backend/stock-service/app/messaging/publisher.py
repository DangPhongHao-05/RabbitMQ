import json
import aio_pika

from app.messaging import rabbitmq


async def publish_stock_event(event_name: str, data: dict):

    if rabbitmq.channel is None:
        raise RuntimeError("RabbitMQ chưa được kết nối!")

    exchange = await rabbitmq.channel.declare_exchange(
        "stock.events", aio_pika.ExchangeType.TOPIC, durable=True
    )

    message_data = {"event": event_name, "data": data}

    await exchange.publish(
        aio_pika.Message(
            body=json.dumps(message_data).encode(), content_type="application/json"
        ),
        routing_key=event_name,
    )

    print(f"Đã phát sự kiện: {event_name}")
