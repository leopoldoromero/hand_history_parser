from app.stats_generator.game_state_handler import GameStateHandler
from collections import defaultdict

class StatsGenerator:
    def __init__(self, hands):
        self.hands = hands
        self.players_stats = defaultdict(lambda: defaultdict(int))
        self.state_handler = GameStateHandler(self.players_stats)

    def get_pot_type(self): 
        return self.state_handler.state
    
    def is_preflop(self, action):
        return action["phase"] == "PRE-FLOP"
    
    def three_bet_opp_handle(self, action, player, state):
        if state in ["OPEN_RAISED", "ROL_RAISED"] and action in ["fold", "call", "raise"]:
            self.players_stats[player]["3BET_OPP"] += 1


    def process_hand(self, hand):
        pre_flop_actions = list(filter(self.is_preflop, hand["actions"]))
        all_players = [action["player"] for action in hand["actions"] if "player" in action]
        small_blind = next((action["player"] for action in hand["actions"] if action["action"] == "small_blind"), None)
        big_blind = next((action["player"] for action in hand["actions"] if action["action"] == "big_blind"), None)

        players_order = [p for p in all_players if p not in (small_blind, big_blind)]
        if small_blind:
            players_order.append(small_blind)
        if big_blind:
            players_order.append(big_blind)

        # state_handler = GameStateHandler(self.players_stats)
        self.state_handler.metadata["player_order"] = players_order

        for action in pre_flop_actions:
            player = action["player"]
            action_name = action["action"]
            self.three_bet_opp_handle(action_name, player, self.state_handler.state)
            self.state_handler.handle_action(player, action_name)

        for key in self.players_stats:
          if key in players_order:
            self.players_stats[key]["HANDS"] += 1

    def calculate_vpip(self, hands_played, hands_folded):
        return (hands_played - hands_folded) / hands_played * 100

    def calculate_pfr(self, hands_played, hands_raised):
        return hands_raised / hands_played * 100
    
    def calculate_aggression_factor(self, hands_raised, calls):
        return (hands_raised) / calls if calls != 0 else 0
    
    def calculate_3bet_percentage(self, total_3bets, opportunities):
        return (total_3bets / opportunities * 100) if opportunities > 0 else 0.0

    def execute(self):
        for hand in self.hands:
            self.process_hand(hand)

        for player_name, stats in self.players_stats.items():
            #hands_folded = stats["FOLD_TO_3BET"] + stats["FOLD_TO_SQUEEZE"] + stats["FOLD_TO_4BET"]

            vpip = self.calculate_vpip(stats["HANDS"], stats["FOLD"])
            hands_raised = stats["OR"] + stats["ROL"] + stats["3BET"] + stats["SQUEEZE"] + stats["4BET"]
            pfr = self.calculate_pfr(stats["HANDS"], hands_raised)
            three_bet_percentage = self.calculate_3bet_percentage(stats["3BET"] + stats["SQUEEZE"], stats["3BET_OPP"])
            stats["VPIP"] = round(vpip, 2)
            stats["PFR"] = round(pfr, 2)
            stats["3BET%"] = round(three_bet_percentage, 2)
            # af = self.calculate_aggression_factor(hands_raised)
            # stats["AF"] = af

        return self.players_stats