import os
from dotenv import load_dotenv

load_dotenv()

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://127.0.0.1:8001")

STOCK_SERVICE_URL = os.getenv("STOCK_SERVICE_URL", "http://127.0.0.1:8002")

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
