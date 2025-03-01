from pydantic import BaseModel


class DeleteHandsResponseDto(BaseModel):
    success: bool
