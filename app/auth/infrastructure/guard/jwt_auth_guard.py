from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError
from app.shared.config.app_config import JWT_SECRET_KEY, JWT_ALGORITHM
# from app.auth.domain.exceptions.invalid_credentials_exception import (
#     InvalidCredentialsException,
# )
# from app.auth.infrastructure.jwt.jwt_handler import JwtHandler

security = HTTPBearer()


def auth_guard(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    except Exception as e:
        print(f"Auth Guard Error: {e}")
        raise HTTPException(status_code=500, detail="Authentication failed")
