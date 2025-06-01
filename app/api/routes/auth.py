import jwt
from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

# Secret key & Algorithm
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/v1", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


# Fake user database
fake_users_db = {
    "user1@example.com": {  # Now using email as the key
        "id": "75565b68-ed1f-11ef-901b-0ade7a4f7cd3",
        "username": "user1",
        "full_name": "John Doe",
        "email": "user1@example.com",
        "hashed_password": "$2b$12$IU5OvHGBRT7vEfO/j5b9Z.7f5Pao8u.xhsxvWXcF5R4jeqcdAS4/m",
    }
}

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# # Verify password
def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        raise Exception(e)


# # Create JWT token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# # Authenticate user
def authenticate_user(email: str, password: str):
    user = fake_users_db.get(email)
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user


@router.get("/generate")
def generate_pass():
    # Hash the password with bcrypt
    password_to_hash = "testpassword123"
    hashed_password = pwd_context.hash(password_to_hash)
    return {"hashed_password": hashed_password}


@router.post("/token")
def login_for_access_token(login_data: LoginRequest):
    user = authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user["id"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}


# Protected route
# @router.get("/users/me")
# def read_users_me(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     return {"id": user_id}
