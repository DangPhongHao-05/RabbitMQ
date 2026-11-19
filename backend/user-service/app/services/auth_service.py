from bson import ObjectId
from pwdlib import PasswordHash
from fastapi import HTTPException, status

from app.schemas.user import UserRegister, UserLogin

# Khởi tạo công cụ mã hóa mật khẩu
password_hash = PasswordHash.recommended()


# Đăng ký
async def register_user(db, data: UserRegister):

    # Kiểm tra username đã tồn tại chưa
    existing_user = await db.users.find_one({"username": data.username})

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username đã tồn tại"
        )

    # Mã hóa mật khẩu
    hashed_password = password_hash.hash(data.password)

    # Tạo document người dùng
    new_user = {
        "username": data.username,
        "password": hashed_password,
        "fullname": data.fullname,
    }

    # Lưu vào MongoDB
    result = await db.users.insert_one(new_user)

    return {
        "id": str(result.inserted_id),
        "username": data.username,
        "fullname": data.fullname,
    }


# Đăng nhập
async def login_user(db, data: UserLogin):

    # Tìm người dùng theo username
    user = await db.users.find_one({"username": data.username})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username hoặc password không đúng",
        )

    # Kiểm tra password
    is_password_correct = password_hash.verify(data.password, user["password"])

    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username hoặc password không đúng",
        )

    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "fullname": user["fullname"],
    }


# Lấy thông tin người dùng theo ID
async def get_user_by_id(db, user_id: str):

    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID người dùng không hợp lệ"
        )

    user = await db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng"
        )

    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "fullname": user["fullname"],
    }
