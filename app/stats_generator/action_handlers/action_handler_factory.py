from app.stats_generator.action_handlers.unopened_handler import UnopenedHandler
from app.stats_generator.action_handlers.limp_handler import LimpHandler
from app.stats_generator.action_handlers.or_handler import ORHandler
from app.stats_generator.action_handlers.rol_handler import RolHandler
from app.stats_generator.action_handlers.three_bet_handler import ThreeBetHandler
from app.stats_generator.action_handlers.squeeze_handler import SqueezeHandler
from app.stats_generator.action_handlers.four_bet_handler import FourBetHandler


class ActionHandlerFactory:
    _handlers = {
        "UNOPENED": UnopenedHandler,
        "LIMPED": LimpHandler,
        "OPEN_RAISED": ORHandler,
        "ROL_RAISED": RolHandler,
        "3BET": ThreeBetHandler,
        "SQUEEZE": SqueezeHandler,
        "4BET": FourBetHandler,
    }

    @staticmethod
    def get_handler(state):
        handler = ActionHandlerFactory._handlers.get(state)
        return handler() if handler else None
