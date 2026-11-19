from fastapi import APIRouter, Request, Header, HTTPException

from app.schemas.stock import StockCreate
from app.messaging.rabbitmq import verify_user

from app.services.stock_service import (
    get_stocks,
    create_stock,
    update_stock,
    delete_stock,
)

router = APIRouter(prefix="/stocks", tags=["Stocks"])


# Hàm xác minh người dùng qua RabbitMQ
async def check_user(user_id: str):
    try:
        result = await verify_user(user_id)

        if not result.get("exists"):
            raise HTTPException(
                status_code=401,
                detail="Người dùng không tồn tại!",
            )

        return result["user"]

    except TimeoutError:
        raise HTTPException(
            status_code=503,
            detail="User Service không phản hồi!",
        )


# GET: Lấy danh sách cổ phiếu
@router.get("/")
async def get_all_stocks(request: Request):
    db = request.app.state.db

    stocks = await get_stocks(db)

    return stocks


# POST: Thêm cổ phiếu
@router.post("/")
async def add_stock(
    data: StockCreate,
    request: Request,
    user_id: str = Header(alias="X-User-Id"),
):
    db = request.app.state.db

    user = await check_user(user_id)

    stock = await create_stock(db, data, user["id"])

    return {
        "message": "Thêm cổ phiếu thành công",
        "stock": stock,
    }


# PUT: Cập nhật cổ phiếu
@router.put("/{stock_id}")
async def edit_stock(
    stock_id: str,
    data: StockCreate,
    request: Request,
    user_id: str = Header(alias="X-User-Id"),
):
    db = request.app.state.db

    user = await check_user(user_id)

    stock = await update_stock(db, stock_id, data, user["id"])

    return {
        "message": "Cập nhật cổ phiếu thành công",
        "stock": stock,
    }


# DELETE: Xóa cổ phiếu
@router.delete("/{stock_id}")
async def remove_stock(
    stock_id: str,
    request: Request,
    user_id: str = Header(alias="X-User-Id"),
):
    db = request.app.state.db

    user = await check_user(user_id)

    result = await delete_stock(db, stock_id, user["id"])

    return result
