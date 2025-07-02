from app.hand.domain.hand import Hand
from app.hand.domain.stats import PlayerStats, Stats
from app.hand.application.game_state_handler import GameStateHandler


class StatsGenerator:
    def __init__(self, hands):
        self.hands = hands
        self.players_stats = []

    def is_preflop(self, action):
        return action.phase == "PRE-FLOP"

    def three_bet_opp_handle(self, action, player, state):
        if state in ["OPEN_RAISED", "ROL_RAISED"] and action in [
            "fold",
            "call",
            "raise",
        ]:
            player_stat = next(
                (ps for ps in self.players_stats if ps.name == player), None
            )
            if not player_stat:
                raise ValueError(
                    f"Player '{player}' not found in stats list. StatsGenerator"
                )
            player_stat.increment("three_bet_opp")

    def process_hand(self, hand: Hand):
        print(f"Procceesing hand: {hand.general_info.room_hand_id}")
        pre_flop_actions = list(filter(self.is_preflop, hand.actions))
        all_players = [action.player for action in hand.actions if action.player]
        small_blind = next(
            (
                action.player
                for action in hand.actions
                if action.action == "small_blind"
            ),
            None,
        )
        big_blind = next(
            (action.player for action in hand.actions if action.action == "big_blind"),
            None,
        )

        players_order = [p for p in all_players if p not in (small_blind, big_blind)]
        if small_blind:
            players_order.append(small_blind)
        if big_blind:
            players_order.append(big_blind)

        if len(self.players_stats) == 0:
            self.players_stats = [PlayerStats(name=player) for player in players_order]
        else:
            current_players = [ps.name for ps in self.players_stats]
            self.players_stats = self.players_stats + [
                PlayerStats(name=player)
                for player in players_order
                if player not in current_players
            ]
        state_handler = GameStateHandler(self.players_stats)
        state_handler.metadata["player_order"] = players_order

        for action in pre_flop_actions:
            player = action.player
            action_name = action.action
            self.three_bet_opp_handle(action_name, player, state_handler.state)
            state_handler.handle_action(player, action_name)

        for player in set(players_order):
            player_stat = next(
                (ps for ps in self.players_stats if ps.name == player), None
            )
            if not player_stat:
                raise ValueError(
                    f"Player '{player}' not found in stats list. StatsGenerator"
                )
            player_stat.increment("hands")

    def calculate_vpip(self, hands_played, stats):
        voluntary = (
            stats.limp
            + stats.open_raise
            + stats.rol
            + stats.three_bet
            + stats.squeeze
            + stats.four_bet
        )
        return (voluntary / hands_played) * 100 if hands_played else 0.0

    def calculate_pfr(self, hands_played, hands_raised):
        return hands_raised / hands_played * 100 if hands_played else 0.0

    def calculate_3bet_percentage(self, total_3bets, opportunities):
        return (total_3bets / opportunities * 100) if opportunities else 0.0

    def execute(self, user_id: str):
        for hand in self.hands:
            self.process_hand(hand)

        for stats in self.players_stats:
            vpip = self.calculate_vpip(stats.hands, stats)
            hands_raised = (
                stats.open_raise
                + stats.rol
                + stats.three_bet
                + stats.squeeze
                + stats.four_bet
            )
            pfr = self.calculate_pfr(stats.hands, hands_raised)
            three_bet_percentage = self.calculate_3bet_percentage(
                stats.three_bet + stats.squeeze, stats.three_bet_opp
            )

            stats.set_att("vpip", round(vpip, 2))
            stats.set_att("pfr", round(pfr, 2))
            stats.set_att("three_bet_percent", round(three_bet_percentage, 2))
            stats.set_att("is_hero", stats.name == self.hands[0].hero_name)

        return Stats(user_id, self.players_stats)
