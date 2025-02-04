from app.stats_generator.game_state_handler import GameStateHandler
from collections import defaultdict

class StatsGenerator:
    def __init__(self, hands):
        self.hands = hands
        self.players_stats = defaultdict(lambda: defaultdict(int))

    def is_preflop(self, action):
        return action["phase"] == "PRE-FLOP"

    def process_hand(self, hand):
        pre_flop_actions = list(filter(self.is_preflop, hand["actions"]))

        # Extract player order, ensuring blinds act last
        all_players = [action["player"] for action in hand["actions"] if "player" in action]
        small_blind = next((action["player"] for action in hand["actions"] if action["action"] == "small_blind"), None)
        big_blind = next((action["player"] for action in hand["actions"] if action["action"] == "big_blind"), None)

        players_order = [p for p in all_players if p not in (small_blind, big_blind)]
        if small_blind:
            players_order.append(small_blind)
        if big_blind:
            players_order.append(big_blind)

        # Initialize StateHandler once per hand
        state_handler = GameStateHandler(self.players_stats)
        state_handler.metadata["player_order"] = players_order

        # Process pre-flop actions
        for action in pre_flop_actions:
            player = action["player"]
            state_handler.handle_action(player, action["action"])

        # Update hands count
        for key in self.players_stats:
          if key in players_order:
            self.players_stats[key]["HANDS"] += 1

    def execute(self):
        for hand in self.hands:
            self.process_hand(hand)
        return self.players_stats