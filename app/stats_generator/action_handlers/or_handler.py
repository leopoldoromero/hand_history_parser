class ORHandler:
    def handle(self, action, player, metadata):
        if action == "call":
            return {
                "stat": "call_to_or",
                "new_state": "OPEN_RAISED",
                "metadata_updates": {"callers": metadata.get("callers", []) + [player]},
            }

        if action == "raise":
            stat = "squeeze" if len(metadata["callers"]) > 0 else "three_bet"
            new_state = "SQUEEZE" if len(metadata["callers"]) > 0 else "3BET"

            return {
                "stat": stat,
                "new_state": new_state,
                "metadata_updates": {
                    "last_aggressor": player,
                    "facing_players": [metadata["last_aggressor"]],
                },
            }

        if action == "fold":
            if player in metadata["facing_players"]:
                return {
                    "stat": "fold_to_3bet",
                    "new_state": "OPEN_RAISED",
                    "metadata_updates": {},
                }
