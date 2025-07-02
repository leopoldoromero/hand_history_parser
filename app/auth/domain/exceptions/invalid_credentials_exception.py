from app.shared.domain import BaseAppException, ErrorCode


class InvalidCredentialsException(BaseAppException):
    def __init__(self):
        super().__init__(
            message="Invalid email or password", code=ErrorCode.INVALID_CREDENTIALS
        )
