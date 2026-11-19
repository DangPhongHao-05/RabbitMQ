from fastapi import APIRouter, Request

from app.config import STOCK_SERVICE_URL
from app.proxy import proxy_request

router = APIRouter()


@router.api_route("/api/stocks", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
@router.api_route(
    "/api/stocks/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
)
async def stock_proxy(request: Request, path: str = ""):

    target_url = f"{STOCK_SERVICE_URL}/stocks"

    if path:
        target_url += f"/{path}"
    elif request.method in ["GET", "POST"]:
        target_url += "/"

    return await proxy_request(request, target_url)
