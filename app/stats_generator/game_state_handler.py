from app.stats_generator.action_handlers.action_handler_factory import ActionHandlerFactory

class GameStateHandler:
    DEFAULT_STATS = {
        "HANDS": 0,
        "FOLD": 0,
        "LIMP": 0,
        "OR": 0,
        "ROL": 0,
        "3BET": 0,
        "SQUEEZE": 0,
        "4BET": 0,
        "CALL_TO_OR": 0,
        "CALL_TO_ROL" : 0,
        "CALL_TO_3BET": 0,
        "CALL_TO_SQUEEZE": 0,
        "CALL_TO_4BET": 0,
        "FOLD_TO_3BET": 0,
        "FOLD_TO_SQUEEZE": 0,
        "FOLD_TO_4BET": 0,
    }

    def __init__(self, player_stats):
        self.state = "UNOPENED"
        self.metadata = {
            "last_aggressor": None,  # Player who last raised
            "callers": [],           # Players who called the last aggressor’s bet
            "facing_players": [],    # Players who must act (e.g., facing a 3-bet)
            "player_order": []       # Track player positions (e.g., ["P1", "P2", "P3"])
        }
        self.player_stats = player_stats
        self.handler_factory = ActionHandlerFactory()

    def get_players_to_act(self, current_player):
        """Get players left to act after the current aggressor."""
        idx = self.metadata["player_order"].index(current_player)
        return self.metadata["player_order"][idx + 1:]

    def handle_action(self, player, action):
        """Handles a player's action using the appropriate handler."""
        if action == "fold" and player not in self.metadata["facing_players"]:
          self.update_player_stat(player, "FOLD")
          return
        handler = self.handler_factory.get_handler(self.state)
        if not handler:
            return  # No valid handler for the current state

        result = handler.handle(action, player, self.metadata)
        if not result:
            return  # No valid transition

        # Handle conditions
        if "condition" in result and not result["condition"]:
            return  # Condition not met

        # Update stats
        self.update_player_stat(player, result["stat"])

        # Update state
        self.state = result["new_state"]

        # Update metadata
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

    def update_player_stat(self, player, stat):
        """Update the player's stats."""
        if player not in self.player_stats:
            self.player_stats[player] = self.DEFAULT_STATS.copy()
        self.player_stats[player][stat] += 1
