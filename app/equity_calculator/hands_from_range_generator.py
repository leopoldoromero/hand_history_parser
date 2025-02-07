from itertools import product, combinations

class HandsFromRangeGenerator:

    def generate(self, range_list, excluded_cards):
        """
        Generate all valid hole card combinations from a given hand range.
        Excludes hands containing known cards (e.g., board and hero's hand).
        
        :param range_list: List of hand combos like ["AQs", "AQo", "JJ"]
        :param excluded_cards: List of already known cards (board, hero hand)
        :return: List of all possible hands matching the range
        """
        all_hands = []
        suits = ["s", "h", "d", "c"]

        for hand in range_list:
            rank1, rank2 = hand[:2]  # Extract rank
            suited = hand[2:] if len(hand) == 3 else None  # "s" or "o" or empty

            possible_hands = []

            if rank1 == rank2:  # Pocket pairs (e.g., "JJ")
                for suit1, suit2 in combinations(suits, 2):  # All suit combos
                    hole_cards = [rank1 + suit1, rank2 + suit2]
                    
                    if not any(c in excluded_cards for c in hole_cards):
                        possible_hands.append(hole_cards)

            else:  # Non-pocket pair hands
                for suit1, suit2 in product(suits, repeat=2):
                    if suited == "s" and suit1 != suit2:
                        continue  # Skip offsuit if suited-only
                    if suited == "o" and suit1 == suit2:
                        continue  # Skip suited if offsuit-only
                    
                    hole_cards = [rank1 + suit1, rank2 + suit2]

                    if not any(c in excluded_cards for c in hole_cards):
                        possible_hands.append(hole_cards)

            all_hands.extend(possible_hands)

        return all_hands