class SqueezeHandler():
  def handle(self, action, player, metadata):
    if action == "call":
      return {
        "stat": "CALL_TO_SQUEEZE",
        "new_state": "SQUEEZE",
        "metadata_updates": {"callers": [player]}
      }
    if action == "raise":
      return {
        "stat": "4BET",
        "new_state": "4BET",
        "metadata_updates": {
          "last_aggressor": player,
          "facing_players": [metadata["last_aggressor"]]
        }
      }
    condition = player in metadata["facing_players"]
    return {
      "condition": condition,
      "stat": "FOLD_TO_SQUEEZE",
      "new_state": "SQUEEZE"
    }