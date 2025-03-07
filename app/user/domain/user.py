import uuid


class User:
    def __init__(self, id: str, email: str, password: str) -> None:
        self.id = id if id else str(uuid.uuid4())
        self.email = email
        self.password = password

    @staticmethod
    def create(email: str, password: str) -> "User":
        return User(id=str(uuid.uuid4()), email=email, password=password)
