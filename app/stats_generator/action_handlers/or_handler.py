class ORHandler():
    def handle(self, action, player, metadata):
        if action == "call":
            return {
                "stat": "CALL_TO_OR",
                "new_state": "OPEN_RAISED",
                "metadata_updates": {"callers": metadata.get("callers", []) + [player]}
            }
        
        if action == "raise":
            stat = "SQUEEZE" if len(metadata["callers"]) > 0 else "3BET"
            new_state = "SQUEEZE" if len(metadata["callers"]) > 0 else "3BET"
            
            return {
                "stat": stat,
                "new_state": new_state,
                "metadata_updates": {
                    "last_aggressor": player,
                    "facing_players": [metadata["last_aggressor"]]
                }
            }

        if action == "fold":
            if player in metadata["facing_players"]:
                return {
                    "stat": "FOLD_TO_3BET",
                    "new_state": "OPEN_RAISED",
                    "metadata_updates": {}
                }