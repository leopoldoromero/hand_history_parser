from app.shared.domain import ErrorCode


class BaseAppException(Exception):
    def __init__(self, message: str, code: ErrorCode):
        self.message = message
        self.code = code

    def to_dict(self):
        return {
            "message": self.message,
            "code": self.code.value if hasattr(self.code, "value") else self.code,
        }
