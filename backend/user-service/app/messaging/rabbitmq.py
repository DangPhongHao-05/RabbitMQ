import json
import aio_pika

from bson import ObjectId
from app.config import settings
from app.database import get_database

connection = None
channel = None
queue = None
consumer_tag = None


# Kết nối RabbitMQ
async def connect_rabbitmq():

    global connection, channel

    connection = await aio_pika.connect_robust(
        settings.rabbitmq_url, client_properties={"connection_name": "user-service"}
    )

    channel = await connection.channel()

    print("Connected to RabbitMQ successfully!")


# Xử lý yêu cầu kiểm tra người dùng
async def handle_verify_user(message: aio_pika.IncomingMessage):

    async with message.process():

        # Đọc dữ liệu JSON từ message
        data = json.loads(message.body.decode())

        user_id = data.get("user_id")

        db = get_database()

        user = None

        # Kiểm tra ID hợp lệ
        if user_id and ObjectId.is_valid(user_id):

            user = await db.users.find_one({"_id": ObjectId(user_id)})

        # Xây dựng kết quả trả về
        if user:
            response_data = {
                "exists": True,
                "user": {
                    "id": str(user["_id"]),
                    "username": user["username"],
                    "fullname": user.get("fullname", ""),
                },
            }
        else:
            response_data = {"exists": False, "user": None}

        # Gửi kết quả về queue của bên yêu cầu
        if message.reply_to:

            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(response_data).encode(),
                    correlation_id=message.correlation_id,
                ),
                routing_key=message.reply_to,
            )


# Khởi động Consumer
async def start_user_consumer():

    global queue, consumer_tag

    queue = await channel.declare_queue("user.verify", durable=True)

    consumer_tag = await queue.consume(handle_verify_user)

    print("User Service is listening to user.verify")


# Đóng kết nối RabbitMQ
async def close_rabbitmq():

    global connection, queue, consumer_tag

    if queue and consumer_tag:
        await queue.cancel(consumer_tag)

    if connection and not connection.is_closed:
        await connection.close()

    print("RabbitMQ connection closed!")
