from pydantic import BaseModel, EmailStr
from app.user.domain.user import User

class UserSchema(BaseModel):
    id: str = None 
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

    @staticmethod
    def from_domain(user: User) -> "UserSchema":
        """Creates a UserSchema instance from a domain User instance."""
        return UserSchema(
            id=user.id,
            email=user.email,
            password=user.password
        )
