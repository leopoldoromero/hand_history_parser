class RolHandler:
    def handle(self, action, player, metadata):
        if action == "call":
            return {
                "stat": "call_to_rol",
                "new_state": "ROL_RAISED",
                "metadata_updates": {"callers": [player]},
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
