from motor.motor_asyncio import AsyncIOMotorClient
from app.shared.config.app_config import (
    MONGODB_URL,
    MAX_CONNECTIONS_COUNT,
    MIN_CONNECTIONS_COUNT,
    database_name,
)


class DataBase:
    client: AsyncIOMotorClient = None

    async def connect_to_mongo(self):
        print("Conecting to mongoDb...")
        self.client = AsyncIOMotorClient(
            str(MONGODB_URL),
            maxPoolSize=MAX_CONNECTIONS_COUNT,
            minPoolSize=MIN_CONNECTIONS_COUNT,
        )
        print("Conected to mongoDb")

    async def close_mongo_connection(self):
        print("Closing mongoDb conection...")
        self.client.close()
        print("MongoDb conection closed")

    def get_collection(self, collection_name: str):
        return self.client[database_name][collection_name]


mongoDbClient = DataBase()
