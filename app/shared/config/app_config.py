import os
from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings, Secret
from databases import DatabaseURL

load_dotenv(".env")

APPLICATION_TITLE = "Poker hand history parser"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ACCESS_TOKEN_EXPIRE_DAYS = 7
ACCESS_TOKEN_COOKIE_MAX_AGE = 60 * 30  # 30 minutes
REFRESH_TOKEN_COOKIE_MAX_AGE = 60 * 60 * 24 * 7  # 7 days
GUEST_ID_COOKIE_MAX_AGE = 60 * 60 * 24 * 7  # 7 days
JWT_ALGORITHM = "HS256"
OPENAPI_PATH = "/api/v1/openapi.json"
DEFAULT_USER_ID = "75565b68-ed1f-11ef-901b-0ade7a4f7cd3"

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
JWT_SECRET_KEY = Secret(os.getenv("JWT_SECRET_KEY", "ssupersecretkey"))

ALLOWED_HOSTS = CommaSeparatedStrings(
    os.getenv("ALLOWED_HOSTS", "http://localhost:3000")
)

MONGODB_URL = os.getenv("MONGODB_URL", "")
MONGO_DB = os.getenv("MONGO_DB", "hand_replayer")

if not MONGODB_URL:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USER = os.getenv("MONGO_USER", "admin")
    MONGO_PASS = os.getenv("MONGO_PASSWORD", "password")

    MONGODB_URL = DatabaseURL(
        f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
    )
else:
    MONGODB_URL = DatabaseURL(MONGODB_URL)
