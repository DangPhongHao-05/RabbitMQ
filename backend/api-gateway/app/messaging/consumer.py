import json
import aio_pika

from app.services.websocket_manager import manager

connection = None
channel = None
queue = None
consumer_tag = None


# Kết nối RabbitMQ và bắt đầu lắng nghe sự kiện
async def start_stock_consumer(rabbitmq_url: str):

    global connection, channel, consumer_tag

    connection = await aio_pika.connect_robust(rabbitmq_url)
    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        "stock.events", aio_pika.ExchangeType.TOPIC, durable=True
    )

    # Queue riêng dành cho API Gateway
    queue = await channel.declare_queue(
        "api-gateway.stock-events", durable=False, exclusive=True, auto_delete=True
    )

    # Nhận tất cả sự kiện cổ phiếu
    await queue.bind(exchange, routing_key="stock.*")

    async def process_message(message: aio_pika.IncomingMessage):

        async with message.process():

            event_data = json.loads(message.body.decode())

            print("Nhận sự kiện:", event_data)

            # Gửi sự kiện đến các trình duyệt đang kết nối
            await manager.broadcast(event_data)

    consumer_tag = await queue.consume(process_message)

    print("API Gateway đang lắng nghe stock.events!")


# Đóng kết nối RabbitMQ
async def stop_stock_consumer():

    global connection, channel, consumer_tag

    if channel and consumer_tag:
        await channel.cancel(consumer_tag)

    if connection and not connection.is_closed:
        await connection.close()

    connection = None
    channel = None
    consumer_tag = None

    print("API Gateway đã ngắt kết nối RabbitMQ!")
