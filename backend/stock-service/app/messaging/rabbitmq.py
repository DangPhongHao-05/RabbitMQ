import asyncio
import json
import uuid

import aio_pika

from app.config import settings

connection = None
channel = None


async def connect_rabbitmq():
    global connection, channel

    connection = await aio_pika.connect_robust(
        settings.rabbitmq_url, client_properties={"connection_name": "stock-service"}
    )

    channel = await connection.channel()

    print("Stock Service connected to RabbitMQ!")


async def verify_user(user_id: str):
    if channel is None:
        raise RuntimeError("RabbitMQ chưa được kết nối!")

    callback_queue = await channel.declare_queue(exclusive=True, auto_delete=True)

    correlation_id = str(uuid.uuid4())
    future = asyncio.get_running_loop().create_future()

    async def on_response(message: aio_pika.IncomingMessage):
        if message.correlation_id == correlation_id:
            async with message.process():
                if not future.done():
                    future.set_result(json.loads(message.body.decode()))

    consumer_tag = await callback_queue.consume(on_response)

    request_data = {"user_id": user_id}

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(request_data).encode(),
            reply_to=callback_queue.name,
            correlation_id=correlation_id,
        ),
        routing_key="user.verify",
    )

    print(f"Đã gửi yêu cầu xác minh user: {user_id}")

    try:
        response = await asyncio.wait_for(future, timeout=180)
        return response

    except asyncio.TimeoutError:    
        raise TimeoutError("User Service không phản hồi!")

    finally:
        await callback_queue.cancel(consumer_tag)


async def close_rabbitmq():
    global connection, channel

    if connection and not connection.is_closed:
        await connection.close()

    connection = None
    channel = None

    print("Stock Service disconnected from RabbitMQ!")
