from app.shared.domain import BaseAppException, ErrorCode


class TokenExpiredException(BaseAppException):
    def __init__(self):
        super().__init__("Token expired", ErrorCode.TOKEN_EXPIRED)


class InvalidTokenException(Exception):
    def __init__(self):
        super().__init__("Token invalido", ErrorCode.INVALID_TOKEN)


class InvalidTokenSignatureException(Exception):
    def __init__(self):
        super().__init__("Invalid token signature", ErrorCode.INVALID_SIGNATURE)


class DecodeTokenSignatureException(Exception):
    def __init__(self):
        super().__init__("Token decode error", ErrorCode.DECODE_ERROR)
