import asyncio

from app.messaging.consumer import connect_rabbitmq, start_consumer, close_rabbitmq


async def main():
    try:
        await connect_rabbitmq()
        await start_consumer()

        print("Notification Service is running...")

        await asyncio.Future()

    finally:
        await close_rabbitmq()


if __name__ == "__main__":
    asyncio.run(main())
