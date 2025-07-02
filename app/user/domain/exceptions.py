from app.shared.domain.base_exception import BaseAppException
from app.shared.domain.error_code import ErrorCode


class InvalidEmailException(BaseAppException):
    def __init__(self):
        super().__init__(message="Invalid email address", code=ErrorCode.INVALID_EMAIL)


class InvalidPasswordException(BaseAppException):
    def __init__(self):
        super().__init__(
            message="Password must be at least 6 characters long",
            code=ErrorCode.INVALID_PASSWORD,
        )


class UserAlreadyExistException(BaseAppException):
    def __init__(self):
        super().__init__(
            message="User already exists", code=ErrorCode.USER_ALREADY_EXIST
        )
