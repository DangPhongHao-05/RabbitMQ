import asyncio
import json
import uuid

import aio_pika
from app.config import settings


async def main():
    connection = await aio_pika.connect_robust(settings.rabbitmq_url)

    channel = await connection.channel()

    # Tạo queue nhận kết quả phản hồi
    callback_queue = await channel.declare_queue(exclusive=True)

    # Tạo mã để đối chiếu request và response
    correlation_id = str(uuid.uuid4())

    future = asyncio.get_running_loop().create_future()

    async def on_response(message):
        if message.correlation_id == correlation_id:
            future.set_result(json.loads(message.body.decode()))

    await callback_queue.consume(on_response)

    # Gửi yêu cầu xác minh
    request_data = {"user_id": "6aed3ee8b10d04c02c796592"}

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(request_data).encode(),
            reply_to=callback_queue.name,
            correlation_id=correlation_id,
        ),
        routing_key="user.verify",
    )

    print("Đã gửi yêu cầu xác minh user!")

    try:
        response = await asyncio.wait_for(future, timeout=10)

        print("Kết quả phản hồi:", response)

    except asyncio.TimeoutError:
        print("Không nhận được phản hồi!")

    await connection.close()


asyncio.run(main())
