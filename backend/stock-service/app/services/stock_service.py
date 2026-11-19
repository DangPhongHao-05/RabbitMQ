from bson import ObjectId
from fastapi import HTTPException, status

from app.schemas.stock import StockCreate
from app.messaging.publisher import publish_stock_event


# Lấy danh sách cổ phiếu
async def get_stocks(db):

    stocks = []

    cursor = db.stocks.find()

    async for stock in cursor:
        stocks.append(
            {
                "id": str(stock["_id"]),
                "name": stock["name"],
                "code": stock["code"],
                "price": stock["price"],
                "previousPrice": stock["previousPrice"],
                "exchange": stock["exchange"],
                "favorite": stock["favorite"],
                "created_by": stock["created_by"],
            }
        )

    return stocks


# thêm
async def create_stock(db, data: StockCreate, user_id: str):
    existing_stock = await db.stocks.find_one({"code": data.code})

    if existing_stock:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Mã cổ phiếu đã tồn tại"
        )

    new_stock = data.model_dump()
    new_stock["created_by"] = user_id

    result = await db.stocks.insert_one(new_stock)

    stock = {
        "id": str(result.inserted_id),
        "name": new_stock["name"],
        "code": new_stock["code"],
        "price": new_stock["price"],
        "previousPrice": new_stock["previousPrice"],
        "exchange": new_stock["exchange"],
        "favorite": new_stock["favorite"],
        "created_by": new_stock["created_by"],
    }

    # Phát sự kiện sau khi tạo cổ phiếu thành công
    await publish_stock_event("stock.created", stock)

    return stock


# Cập nhật cổ phiếu
async def update_stock(db, stock_id: str, data: StockCreate, user_id: str):

    # Kiểm tra ID hợp lệ
    if not ObjectId.is_valid(stock_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID cổ phiếu không hợp lệ"
        )

    # Tìm cổ phiếu do người dùng này tạo
    stock = await db.stocks.find_one({"_id": ObjectId(stock_id), "created_by": user_id})

    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy cổ phiếu hoặc bạn không có quyền chỉnh sửa",
        )

    # Dữ liệu cập nhật
    update_data = data.model_dump()

    await db.stocks.update_one(
        {"_id": ObjectId(stock_id), "created_by": user_id}, {"$set": update_data}
    )

    stock.update(update_data)

    stock["id"] = str(stock["_id"])
    del stock["_id"]

    await publish_stock_event("stock.updated", stock)

    return stock


# Xóa cổ phiếu
async def delete_stock(db, stock_id: str, user_id: str):

    if not ObjectId.is_valid(stock_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID cổ phiếu không hợp lệ",
        )

    # Tìm cổ phiếu trước khi xóa để lấy thông tin gửi thông báo
    stock = await db.stocks.find_one({"_id": ObjectId(stock_id), "created_by": user_id})

    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy cổ phiếu hoặc bạn không có quyền xóa",
        )

    # Xóa cổ phiếu
    result = await db.stocks.delete_one(
        {"_id": ObjectId(stock_id), "created_by": user_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không thể xóa cổ phiếu",
        )

    # Phát sự kiện sau khi xóa thành công
    await publish_stock_event(
        "stock.deleted",
        {
            "id": str(stock["_id"]),
            "name": stock["name"],
            "code": stock["code"],
        },
    )

    return {"message": "Xóa cổ phiếu thành công"}
