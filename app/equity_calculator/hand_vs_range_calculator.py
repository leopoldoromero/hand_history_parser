import random
from treys import Evaluator, Card
from app.equity_calculator.hands_from_range_generator import HandsFromRangeGenerator

evaluator = Evaluator()

class HandVsRangeEquityCalculator:
    def __init__(self):
        self.range_generator = HandsFromRangeGenerator()

    def convert_card(self, card):
        """Converts a human-readable card format (e.g., "As") to Treys format."""
        rank_map = {'2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', 
                    '8': '8', '9': '9', 'T': 'T', 'J': 'J', 'Q': 'Q', 'K': 'K', 'A': 'A'}
        #suit_map = {'♠': 's', '♥': 'h', '♦': 'd', '♣': 'c'}
        suit_map = {'s': 's', 'h': 'h', 'd': 'd', 'c': 'c'}
        return Card.new(rank_map[card[0]] + suit_map[card[1]])

    def convert_hand(self, hand):
        """Converts a list of human-readable cards (e.g., ["As", "Kc"]) to Treys format."""
        return [self.convert_card(card) for card in hand]
    
    def expand_range(self, opponent_range):
        """Expands shorthand range notation like 'JJ+' to explicit hand representations."""
        expanded_range = []
        pocket_pairs = "22 33 44 55 66 77 88 99 TT JJ QQ KK AA".split()
        
        for hand in opponent_range:
            if '+' in hand and len(hand) == 3 and hand[0] == hand[1]:  # Detect pocket pair shorthand like "JJ+"
                start_index = pocket_pairs.index(hand[:2])
                expanded_range.extend(pocket_pairs[start_index:])
            else:
                expanded_range.append(hand)  # Keep suited/offsuit hands as they are
        
        return expanded_range

    def simulate_matchup(self, hand1, hand2, board, num_simulations, deck):
        """
        Simulates matchups between hand1 and hand2 using Monte Carlo, avoiding duplicate cards.
        :param hand1: List of int like [546233, 2343233] representing a player hand in treys format.
        :param hand2: List of int like [546233, 2343233] representing a player hand in treys format.
        :param board: List of int like [546233, 2343233] representing board hadns in treys format.
        :param num_simulations: int that indicates the number of simulations to run.
        :param deck List of int like [546233, 2343233, 435443] representing the available cards in the deck in treys format.
        """
        wins_hand1, wins_hand2, ties = 0, 0, 0
        num_cards_to_deal = 5 - len(board)

        # Ensure drawn cards do not include duplicates
        available_deck = [card for card in deck if card not in hand1 and card not in hand2 and card not in board]


        if len(available_deck) < num_cards_to_deal:
            raise ValueError(f"Not enough cards to deal. Available deck size: {len(available_deck)}, Needed: {num_cards_to_deal}")

        for _ in range(num_simulations):
            new_board = board + random.sample(available_deck, 5 - len(board))

            if len(new_board) != 5 or len(hand1) != 2 or len(hand2) != 2:
                raise ValueError(f"Invalid number of cards: board={len(new_board)}, hand1={len(hand1)}, hand2={len(hand2)}")

            try:
                score1 = evaluator.evaluate(new_board, hand1)
                score2 = evaluator.evaluate(new_board, hand2)
            except KeyError as e:
                print(f"KeyError: {e}")
                raise
            except TypeError as e:
                print(f"TypeError: {e}")
                raise

            if score1 < score2:
                wins_hand1 += 1
            elif score2 < score1:
                wins_hand2 += 1
            else:
                ties += 1

        return wins_hand1, wins_hand2, ties


    def execute(self, hand1, opponent_range, board=[], num_simulations=10000):
        """
        Runs a Monte Carlo simulation of a hand vs an opponent's range.
        :param hand1 List of str representing a player hand (e.g., ["Qs", "Kh"])
        :param opponent_range List of str representing a player range (e.g., ["JJ", "AQs", "AQo", "KQs"])
        :param board List of str representing the cards of the board (e.g., ["As", "Ks", "Js", "Th", "3d"]),
        optional default [].
        :param num_simulations int Indicates the number of simulations to run. 
        optional default 10000
        :returns tuple[float, float, float] with the values that represents the equity of hand1, equity of range, 
        equity of tie (e.g [28.02, 62.11, 9.87]) 
        """

        expanded_range = self.expand_range(opponent_range)
        # Generate deck without known cards
        deck = [Card.new(rank + suit) for rank in "23456789TJQKA" for suit in "shdc"]
        deck = [card for card in deck if card not in hand1 + board]
        
        # Generate all possible opponent hands
        opponent_hands = self.range_generator.generate(expanded_range, excluded_cards=hand1 + board[:])
        opponent_hands = [self.convert_hand(hand) for hand in opponent_hands]

        total_wins1, total_wins2, total_ties = 0, 0, 0
        num_hands = len(opponent_hands)
        hand1 = self.convert_hand(hand1)
        board = self.convert_hand(board)

        for opp_hand in opponent_hands:
            deck_copy = [card for card in deck if card not in opp_hand]  # Exclude opponent's hand from deck

            wins1, wins2, ties = self.simulate_matchup(hand1, opp_hand, board, num_simulations, deck_copy)
 
            total_wins1 += wins1
            total_wins2 += wins2
            total_ties += ties
        if num_simulations * num_hands == 0:
            raise ValueError(f"No hands to simulate, SIMS: {num_simulations}, HANDS: {num_hands}")
        total_sims = num_simulations * num_hands
        equity_hand1 = (total_wins1 ) / total_sims
        equity_range = (total_wins2 ) / total_sims
        tie_percentage = total_ties / total_sims

        return equity_hand1, equity_range, tie_percentage
    

