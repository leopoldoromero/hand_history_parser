import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.shared.infrastructure.cookies.generate_cookie import generate_cookie
from app.shared.config.app_config import GUEST_ID_COOKIE_MAX_AGE


class GuestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        access_token = request.cookies.get("access_token")

        if access_token:
            return response

        guest_id = request.cookies.get("guest_id")

        new_guest_id = None
        if not guest_id:
            new_guest_id = str(uuid.uuid4())

        if new_guest_id:
            response.set_cookie(
                **generate_cookie("guest_id", new_guest_id, GUEST_ID_COOKIE_MAX_AGE)
            )
        return response
