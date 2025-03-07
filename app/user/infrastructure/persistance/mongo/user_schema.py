from pydantic import BaseModel, EmailStr
from app.user.domain.user import User


class UserSchema(BaseModel):
    id: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @staticmethod
    def from_domain(user: User) -> "UserSchema":
        """Creates a UserSchema instance from a domain User instance."""
        return UserSchema(id=user.id, email=user.email, password=user.password)

    def to_domain(self) -> "User":
        return User(id=self.id, email=self.email, password=self.password)
