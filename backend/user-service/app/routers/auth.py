from fastapi import APIRouter, Request

from app.schemas.user import UserRegister, UserLogin

from app.services.auth_service import register_user, login_user, get_user_by_id

router = APIRouter(prefix="/auth", tags=["Authentication"])


# API đăng ký
@router.post("/register")
async def register(data: UserRegister, request: Request):

    db = request.app.state.db

    user = await register_user(db, data)

    return {"message": "Đăng ký thành công", "user": user}


# API đăng nhập
@router.post("/login")
async def login(data: UserLogin, request: Request):

    db = request.app.state.db

    user = await login_user(db, data)

    return {"message": "Đăng nhập thành công", "user": user}


# API lấy thông tin người dùng
@router.get("/{user_id}")
async def get_user(user_id: str, request: Request):

    db = request.app.state.db

    user = await get_user_by_id(db, user_id)

    return {"message": "Lấy thông tin người dùng thành công", "user": user}
