from fastapi import APIRouter, Request

from app.config import USER_SERVICE_URL
from app.proxy import proxy_request

router = APIRouter()


# Đăng ký, đăng nhập
@router.api_route(
    "/api/auth/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
)
async def auth_proxy(path: str, request: Request):

    target_url = f"{USER_SERVICE_URL}/auth/{path}"

    return await proxy_request(request, target_url)


# Các API quản lý user
@router.api_route("/api/users", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
@router.api_route(
    "/api/users/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
)
async def user_proxy(path: str = "", request: Request = None):

    target_url = f"{USER_SERVICE_URL}/users"

    if path:
        target_url += f"/{path}"

    return await proxy_request(request, target_url)
