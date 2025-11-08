from typing import Annotated, Any

from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    success: Annotated[bool, Field(True, description="Indicate request success")]
    message: Annotated[str | None, Field(None, description="Informational message")]
    data: Annotated[Any, Field(None, description="Response data payload")]
    request_id: Annotated[str | None, Field(None, description="Unique request ID")]
