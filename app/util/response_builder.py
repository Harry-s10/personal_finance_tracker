from typing import Any

from fastapi import Request

from app.models.response_model import SuccessResponse


def build_success_response(
    request: Request, data: Any = None, message: str = "Operation successful"
):
    return SuccessResponse(
        data=data,
        message=message,
        request_id=getattr(request.state, "request_id", None),
    )
