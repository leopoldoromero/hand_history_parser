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
from app.auth.infrastructure.jwt.jwt_handler import JwtHandler
from app.auth.application.login import Login
from app.auth.application.authenticator import Authenticator
from app.hand.application.guest_hands_remover import GuestHandsRemover
from app.user.application.user_creator import UserCreator

mongo_db_client = DataBase()

hands_mongo_repository = HandMongoRepository(mongo_db_client)
user_mongo_repository = UserMongoRepository(mongo_db_client)
stats_mongo_repository = StatsMongoRepository(mongo_db_client)
token_handler = JwtHandler()
login = Login(token_handler=token_handler, user_repository=user_mongo_repository)
authenticator = Authenticator(
    token_handler=token_handler, user_repository=user_mongo_repository
)
guest_hands_remover = GuestHandsRemover(hands_mongo_repository, user_mongo_repository)
user_creator = UserCreator(user_repository=user_mongo_repository)

d_container = {
    "mongo_db_client": mongo_db_client,
    "hands_repository": hands_mongo_repository,
    "user_repository": user_mongo_repository,
    "stats_repository": stats_mongo_repository,
    "login": login,
    "authenticator": authenticator,
    "guest_hands_remover": guest_hands_remover,
    "user_creator": user_creator,
    "token_handler": token_handler,
}


def get_dependency(name: str):
    if name not in d_container:
        raise Exception(f"Dependency {name} does not exist in the container")
    return d_container[name]
