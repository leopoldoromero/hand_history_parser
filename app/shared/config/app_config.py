import os

# from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings, Secret
from databases import DatabaseURL

APPLICATION_TITLE = "Poker hand history parser"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
OPENAPI_PATH = "/api/v1/openapi.json"
# load_dotenv(".env")
DEFAULT_USER_ID = "75565b68-ed1f-11ef-901b-0ade7a4f7cd3"

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
SECRET_KEY = Secret(os.getenv("SECRET_KEY", "secret key for project"))

ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", "*"))

MONGODB_URL = os.getenv("MONGODB_URL", "")
if not MONGODB_URL:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USER = os.getenv("MONGO_USER", "admin")
    MONGO_PASS = os.getenv("MONGO_PASSWORD", "password")
    MONGO_DB = os.getenv("MONGO_DB", "hand_replayer")

    MONGODB_URL = DatabaseURL(
        f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
    )
    print(MONGODB_URL)
else:
    MONGODB_URL = DatabaseURL(MONGODB_URL)

database_name = MONGO_DB
users_collection_name = "users"
hands_collection_name = "hands"
