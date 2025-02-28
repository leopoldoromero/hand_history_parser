class LimpHandler:
    def handle(self, action, player, metadata):
        if action == "call":
            return {
                "stat": "limp",
                "new_state": "LIMPED",
                "metadata_updates": {"callers": [player]},
            }
        if action == "raise":
            return {
                "stat": "rol",
                "new_state": "ROL_RAISED",
                "metadata_updates": {
                    "last_aggressor": player,
                    # "facing_players": ["<players_to_act>"] TODO: Review this
                },
            }
