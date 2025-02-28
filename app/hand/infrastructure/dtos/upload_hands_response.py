from pydantic import BaseModel


class UploadHandsResponseDto(BaseModel):
    success: bool
