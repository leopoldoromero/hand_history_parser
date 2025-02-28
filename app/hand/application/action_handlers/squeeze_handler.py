class SqueezeHandler:
    def handle(self, action, player, metadata):
        if action == "call":
            return {
                "stat": "call_to_squeeze",
                "new_state": "SQUEEZE",
                "metadata_updates": {"callers": [player]},
            }
        if action == "raise":
            return {
                "stat": "four_bet",
                "new_state": "4BET",
                "metadata_updates": {
                    "last_aggressor": player,
                    "facing_players": [metadata["last_aggressor"]],
                },
            }
        condition = player in metadata["facing_players"]
        return {
            "condition": condition,
            "stat": "fold_to_squeeze",
            "new_state": "SQUEEZE",
        }
