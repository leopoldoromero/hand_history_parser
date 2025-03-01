from app.stats_generator.action_handlers.action_handler_factory import (
    ActionHandlerFactory,
)


def test_get_handlers_order():
    expected_handlers = list(ActionHandlerFactory._handlers.values())

    for index, (state, handler_class) in enumerate(
        ActionHandlerFactory._handlers.items()
    ):
        obtained_handler = ActionHandlerFactory.get_handler(state)

        assert isinstance(
            obtained_handler, expected_handlers[index]
        ), f"Handler for state '{state}' does not match. Expected: {handler_class}, but got: {obtained_handler.__class__}"
