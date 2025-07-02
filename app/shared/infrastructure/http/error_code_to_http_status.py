from fastapi import status
from app.shared.domain import ErrorCode

ERROR_CODE_TO_HTTP_STATUS = {
    ErrorCode.TOKEN_EXPIRED: status.HTTP_401_UNAUTHORIZED,
    ErrorCode.INVALID_TOKEN: status.HTTP_401_UNAUTHORIZED,
    ErrorCode.PERMISSION_DENIED: status.HTTP_403_FORBIDDEN,
    ErrorCode.USER_NOT_FOUND: status.HTTP_404_NOT_FOUND,
    ErrorCode.INTERNAL_SERVER_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
    ErrorCode.INVALID_CREDENTIALS: status.HTTP_401_UNAUTHORIZED,
    ErrorCode.INVALID_EMAIL: status.HTTP_400_BAD_REQUEST,
    ErrorCode.INVALID_PASSWORD: status.HTTP_400_BAD_REQUEST,
    ErrorCode.USER_ALREADY_EXIST: status.HTTP_409_CONFLICT,
}


def map_error_code_to_status(code: ErrorCode) -> int:
    return ERROR_CODE_TO_HTTP_STATUS.get(code, status.HTTP_400_BAD_REQUEST)
