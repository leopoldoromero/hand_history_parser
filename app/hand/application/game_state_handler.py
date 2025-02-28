from app.hand.application.action_handlers.action_handler_factory import (
    ActionHandlerFactory,
)
from app.hand.domain.stats import PlayerStats
from collections import defaultdict


class GameStateHandler:
    def __init__(self, player_stats: defaultdict[str, PlayerStats]):
        self.state = "UNOPENED"
        self.metadata = {
            "last_aggressor": None,
            "callers": [],
            "facing_players": [],
            "player_order": [],
        }
        self.player_stats = player_stats
        self.handler_factory = ActionHandlerFactory()

    def get_players_to_act(self, current_player):
        """Get players left to act after the current aggressor."""
        idx = self.metadata["player_order"].index(current_player)
        return self.metadata["player_order"][idx + 1 :]

    def handle_action(self, player: str, action: str):
        """Handles a player's action using the appropriate handler."""
        if action == "fold" and player not in self.metadata["facing_players"]:
            self.update_player_stat(player, "fold")
            return

        handler = self.handler_factory.get_handler(self.state)
        if not handler:
            return

        result = handler.handle(action, player, self.metadata)
        if not result:
            return

        if "condition" in result and not result["condition"]:
            return

        self.update_player_stat(player, result["stat"])

        self.state = result["new_state"]

        if "metadata_updates" in result:
            for key, value in result["metadata_updates"].items():
                if value == "<player>":
                    self.metadata[key] = player
                elif key == "callers" and value == ["<player>"]:
                    self.metadata[key].append(player)
                elif key == "facing_players" and value == ["<players_to_act>"]:
                    self.metadata[key] = self.get_players_to_act(player)
                else:
                    self.metadata[key] = value

    def update_player_stat(self, player: str, stat: str):
        """Update the player's stats using the PlayerStats class."""
        self.player_stats[player].__dict__[stat] += 1
