class RolHandler():
  def handle(self, action, player, metadata):
    if action == "call":
      return {
        "stat": "CALL_TO_ROL",
        "new_state": "ROL_RAISED",
        "metadata_updates": {"callers": [player]}
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