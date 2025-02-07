import random
from treys import Evaluator, Card

evaluator = Evaluator()

class HandVsHandEquityCalculator:
    def convert_card(self, card):
        rank_map = {'2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', 
                    '8': '8', '9': '9', 'T': 'T', 'J': 'J', 'Q': 'Q', 'K': 'K', 'A': 'A'}
        suit_map = {'♠': 's', '♥': 'h', '♦': 'd', '♣': 'c'}
        return Card.new(rank_map[card[0]] + suit_map[card[1]])

    # Convert hand strings to Treys format
    def convert_hand(self, hand):
        return [self.convert_card(card) for card in hand]

    # Monte Carlo Simulation to calculate equity
    def monte_carlo_equity(self, hand1, hand2, num_simulations=100000):
        deck = [Card.new(rank + suit) for rank in "23456789TJQKA" for suit in "shdc"]
        hand1 = self.convert_hand(hand1)
        hand2 = self.convert_hand(hand2)

        # Remove known cards from the deck
        for card in hand1 + hand2:
            deck.remove(card)

        wins_hand1 = 0
        wins_hand2 = 0
        ties = 0

        for _ in range(num_simulations):
            board = random.sample(deck, 5)  # Generate a random board
            score1 = evaluator.evaluate(board, hand1)
            score2 = evaluator.evaluate(board, hand2)

            if score1 < score2:  # Lower score means a better hand in Treys
                wins_hand1 += 1
            elif score2 < score1:
                wins_hand2 += 1
            else:
                ties += 1

        equity_hand1 = (wins_hand1 + ties / 2) / num_simulations
        equity_hand2 = (wins_hand2 + ties / 2) / num_simulations

        return equity_hand1, equity_hand2
