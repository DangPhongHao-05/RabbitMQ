import httpx
from fastapi import Request
from fastapi.responses import Response


async def proxy_request(request: Request, target_url: str):

    body = await request.body()

    headers = dict(request.headers)

    # Không chuyển tiếp các header do HTTP client quản lý
    headers.pop("host", None)
    headers.pop("content-length", None)
    headers.pop("connection", None)

    async with httpx.AsyncClient(follow_redirects=True) as client:

        response = await client.request(
            method=request.method,
            url=target_url,
            params=request.query_params,
            content=body,
            headers=headers,
        )

    response_headers = dict(response.headers)

    response_headers.pop("content-encoding", None)
    response_headers.pop("content-length", None)
    response_headers.pop("transfer-encoding", None)
    response_headers.pop("connection", None)

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=response_headers,
    )
