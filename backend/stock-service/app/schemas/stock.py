from pydantic import BaseModel, Field
from typing import Literal


# Dữ liệu gửi khi tạo hoặc cập nhật cổ phiếu
class StockCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    code: str = Field(min_length=1, max_length=10)
    price: float = Field(ge=0)
    previousPrice: float = Field(ge=0)
    exchange: Literal["NASDAQ", "NYSE", "NSE"]
    favorite: bool = False


# Dữ liệu trả về cho frontend
class StockResponse(BaseModel):
    id: str
    name: str
    code: str
    price: float
    previousPrice: float
    exchange: str
    favorite: bool
    created_by: str
