class UnopenedHandler():
    def handle(self, action, player, metadata):
        if action == "call":
          return {
            "stat": "LIMP",
            "new_state": "LIMPED",
            "metadata_updates": {"callers": [player]}
          }
        if action == "raise":
          return {
            "stat": "OR",
            "new_state": "OPEN_RAISED",
            "metadata_updates": {
              "last_aggressor": player,
              #"facing_players": players_to_act] TODO: review later
            }
          }