from fastapi import APIRouter, HTTPException, status
from app.user.application.user_creator import user_creator
from pydantic import BaseModel
from app.user.domain.exceptions.user_already_exist_exception import (
    UserAlreadyExistException,
)

router = APIRouter(prefix="/v1/users", tags=["users"])


class CreateUserRequest(BaseModel):
    email: str
    password: str


@router.post("/")
async def create_user(body: CreateUserRequest):
    try:
        await user_creator.execute(body.email, body.password)
        return {"success": True}

    except UserAlreadyExistException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.detail,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
