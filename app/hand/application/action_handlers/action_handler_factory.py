from app.hand.application.action_handlers.unopened_handler import UnopenedHandler
from app.hand.application.action_handlers.limp_handler import LimpHandler
from app.hand.application.action_handlers.or_handler import ORHandler
from app.hand.application.action_handlers.rol_handler import RolHandler
from app.hand.application.action_handlers.three_bet_handler import ThreeBetHandler
from app.hand.application.action_handlers.squeeze_handler import SqueezeHandler
from app.hand.application.action_handlers.four_bet_handler import FourBetHandler


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
