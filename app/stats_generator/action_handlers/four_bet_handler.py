class FourBetHandler():
  def handle(self, action, player, metadata):
    if action == "call":
      return {
        "stat": "CALL_TO_4BET",
        "new_state": "4BET"
      }
    if action == "fold":
      condition = player in metadata["facing_players"]
      return {
        "condition": condition,
        "stat": "FOLD_TO_4BET",
        "new_state": "4BET"
      }
    # TODO: pending to include raise to 4BET action