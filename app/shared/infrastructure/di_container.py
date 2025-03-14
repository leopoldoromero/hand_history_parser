from app.hand.infrastructure.persistance.mongo.hand_mongo_repository import (
    HandMongoRepository,
)
from app.shared.infrastructure.persistance.mongo.db_client import DataBase
from app.user.infrastructure.persistance.mongo.user_mongo_repository import (
    UserMongoRepository,
)
from app.hand.infrastructure.persistance.mongo.stats_mongo_repository import (
    StatsMongoRepository,
)

mongo_db_client = DataBase()

hands_mongo_repository = HandMongoRepository(mongo_db_client)
users_mongo_repository = UserMongoRepository(mongo_db_client)
stats_mongo_repository = StatsMongoRepository(mongo_db_client)

d_container = {
    "mongo_db_client": mongo_db_client,
    "hands_repository": hands_mongo_repository,
    "users_repository": users_mongo_repository,
    "stats_repository": stats_mongo_repository,
}


def get_dependency(name: str):
    if name not in d_container:
        raise Exception(f"Dependency {name} does not exist in the container")
    return d_container[name]
