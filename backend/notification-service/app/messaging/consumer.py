import aio_pika

from app.config import settings

connection = None
channel = None


async def connect_rabbitmq():
    global connection, channel

    connection = await aio_pika.connect_robust(
        settings.rabbitmq_url,
        client_properties={"connection_name": "notification-service"},
    )

    channel = await connection.channel()

    print("Notification Service connected to RabbitMQ!")


async def handle_stock_event(message: aio_pika.IncomingMessage):
    async with message.process():
        print("\n========== NOTIFICATION ==========")

        print(message.body.decode())

        print("==================================\n")


async def start_consumer():
    exchange = await channel.declare_exchange(
        "stock.events", aio_pika.ExchangeType.TOPIC, durable=True
    )

    queue = await channel.declare_queue("notification.stock", durable=True)

    await queue.bind(exchange, routing_key="stock.#")

    await queue.consume(handle_stock_event)

    print("Notification Service is listening to stock.events!")


async def close_rabbitmq():
    if connection and not connection.is_closed:
        await connection.close()

    print("Notification Service disconnected from RabbitMQ!")
