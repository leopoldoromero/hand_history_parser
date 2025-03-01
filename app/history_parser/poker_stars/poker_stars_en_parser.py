import re
from app.stats_generator.game_state_handler import GameStateHandler
from collections import defaultdict
import uuid
from app.domain.poker_rooms import PokerRoom


class PokerStarsEnglishParser:
    def __init__(self, transcription: str):
        self.transcription = transcription

    def parse(self):
        hands = re.split(r"\*{10,}\s*#\s*\d+\s*\*{10,}", self.transcription)
        parsed_hands = []
        game_type = self.game_type_extractor(self.transcription)

        for hand in hands:
            if not hand.strip():
                continue
            header_info = self.extract_header_info(hand, game_type)
            players = self.extract_players(hand, game_type)
            hero_name, hero_hand = self.extract_hero_info(hand, game_type)
            actions = self.extract_actions(hand, game_type)
            summary = self.extract_summary(hand, game_type, hero_name)
            showdown = self.extract_showdown(hand, game_type)
            finish_before_showdown = self.extract_finish_before_showdown(
                hand, game_type
            )
            table_name, table_type, button_seat = self.extract_table_and_button_info(
                hand, game_type
            )
            processed_hand = {
                "id": str(uuid.uuid4()),
                "general_info": header_info,
                "table_name": table_name,
                "table_type": table_type,
                "button_seat": button_seat,
                "players": players,
                "hero_cards": hero_hand,
                "hero_name": hero_name,
                "hero_seat": summary["hero_seat"] if summary else None,
                "actions": actions,
                "summary": summary,
                "showdown": showdown,
                "finish_before_showdown": finish_before_showdown,
            }

            pot_type = self.define_pot_type(processed_hand)
            print(f"BTN Info: {table_name, table_type, button_seat}")
            print(f"Hero name: {table_name, table_type, button_seat}")
            print(f"SUMMARY: {summary}")
            print(f"POT TYPE: {pot_type}")

            processed_hand["summary"]["pot_type"] = pot_type

            parsed_hands.append(processed_hand)
        return parsed_hands

    def define_pot_type(self, hand):
        state_handler = GameStateHandler(defaultdict(lambda: defaultdict(int)))
        pre_flop_actions = list(
            filter(lambda action: action["phase"] == "PRE-FLOP", hand["actions"])
        )
        all_players = [
            action["player"] for action in hand["actions"] if "player" in action
        ]
        small_blind = next(
            (
                action["player"]
                for action in hand["actions"]
                if action["action"] == "small_blind"
            ),
            None,
        )
        big_blind = next(
            (
                action["player"]
                for action in hand["actions"]
                if action["action"] == "big_blind"
            ),
            None,
        )

        players_order = [p for p in all_players if p not in (small_blind, big_blind)]
        if small_blind:
            players_order.append(small_blind)
        if big_blind:
            players_order.append(big_blind)

        state_handler.metadata["player_order"] = players_order

        for action in pre_flop_actions:
            player = action["player"]
            action_name = action["action"]
            state_handler.handle_action(player, action_name)

        return state_handler.state

    def extract_table_and_button_info(self, hand: str, game_type: str):
        patterns = {
            "zoom": r"Table '(?P<table_name>[\w-]+)' (?P<table_type>[\w-]+) Seat #(?P<button_seat>\d+)",
        }

        pattern = patterns[game_type]

        match = re.search(pattern, hand)
        if match:
            table_name = match.group("table_name")
            table_type = match.group("table_type")
            button_seat = int(match.group("button_seat"))

        return table_name, table_type, button_seat

    def extract_header_info(self, hand: str, game_type: str):
        patterns = {
            "zoom": r"PokerStars Zoom Hand #(?P<hand_id>\d+):.*?\((?P<blinds>.+?)\) - (?P<datetime>\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) CET",
            "regular": r"PokerStars Hand #(?P<hand_id>\d+):.*?\((?P<blinds>.+?)\) - (?P<datetime>\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) CET",
            "tournament": r"",
            "sng": r"",
        }
        pattern = patterns[game_type]
        match = re.search(pattern, hand)

        if match:
            hand_id = match.group("hand_id")
            datetime = match.group("datetime")
            blinds = match.group("blinds") if "blinds" in match.groupdict() else ""
            currency = "€" if "€" in blinds else "$" if blinds else None
            blinds_match = re.search(
                r"((?P<small_blind>[\d.]+)[^0-9]+(?P<big_blind>[\d.]+))", blinds
            )
            if blinds_match:
                blinds = (
                    float(blinds_match.group("small_blind")),
                    float(blinds_match.group("big_blind")),
                )

                return {
                    "room_hand_id": hand_id,
                    "datetime": datetime,
                    "game_type": game_type,
                    "currency": currency,
                    "small_blind": blinds[0] if blinds else None,
                    "big_blind": blinds[1] if blinds else None,
                    "game": "Hold'em",  # Assuming Hold'em for now
                    "room": PokerRoom.STARS.value,
                }

    def extract_players(self, hand: str, game_type: str):
        players = []
        patterns = {
            "zoom": r"Seat (?P<seat>\d+): (?P<name>\S+) \([^\d]*(?P<stack>[\d]+(?:\.\d+)?)\s*in chips\)",
            "regular": r"Seat (?P<seat>\d+): (?P<name>\S+) \([^\d]*(?P<stack>[\d]+(?:\.\d+)?)\s*in chips\)",
            "tournament": r"",
            "sng": r"",
        }
        pattern = patterns[game_type]

        for player_match in re.finditer(pattern, hand):
            player = {
                "seat": int(player_match.group("seat")),
                "name": player_match.group("name"),
                "stack": float(player_match.group("stack")),
            }
            print(f"PLAYER: {player}")
            players.append(
                {
                    "seat": int(player_match.group("seat")),
                    "name": player_match.group("name"),
                    "stack": float(player_match.group("stack")),
                }
            )

        return players

    def extract_hero_info(self, hand: str, game_type: str):
        patterns = {
            "zoom": r"Dealt to (?P<hero>\S+) \[(.*?)\]",
            "regular": r"Dealt to (?P<hero>\S+) \[(.*?)\]",
            "tournament": r"",
            "sng": r"",
        }
        pattern = patterns[game_type]
        hero_hand_match = re.search(pattern, hand)

        if hero_hand_match:
            hero_name = hero_hand_match.group("hero")
            hero_hand = hero_hand_match.group(2).split()
            return hero_name, hero_hand
        raise Exception("Error extracting hero info, pattern doewsnt match.")

    def extract_blinds_actions(self, hand: str, game_type: str):
        result = []
        patterns = {
            "zoom": r"(?P<player>\S+): posts (?P<type>small|big) blind (?P<currency>[^\d\s]+)(?P<amount>\d+\.\d+)",
            "regular": r"(?P<player>\S+): posts (?P<type>small|big) blind (?P<currency>[^\d\s]+)(?P<amount>\d+\.\d+)",
            "tournament": r"",
            "sng": r"",
        }
        pattern = patterns[game_type]

        for blind_match in re.finditer(pattern, hand):
            blind_type = {"small": "small_blind", "big": "big_blind"}[
                blind_match.group("type")
            ]
            amount = float(blind_match.group("amount"))
            result.append(
                {
                    "phase": "PRE-FLOP",
                    "player": blind_match.group("player"),
                    "action": blind_type,
                    "amount": amount,
                    "cards": [],
                }
            )
        return result

    def extract_actions(self, hand: str, game_type: str):
        blinds = self.extract_blinds_actions(hand, game_type)
        result = blinds[:]
        action_phases = ["HOLE CARDS", "FLOP", "TURN", "RIVER"]
        patterns = {
            "zoom": r"(?P<player>\S+): (?P<action>raises|calls|folds|checks|bets)(?: (?P<currency>[^\d\s]+)(?P<amount1>[\d\.]+)(?: to (?P=currency)(?P<amount2>[\d\.]+))?)?",
            "regular": r"(?P<player>\S+): (?P<action>raises|calls|folds|checks|bets)(?: (?P<currency>[^\d\s]+)(?P<amount1>[\d\.]+)(?: to (?P=currency)(?P<amount2>[\d\.]+))?)?",
            "tournament": r"",
            "sng": r"",
        }
        pattern = patterns[game_type]

        for phase in action_phases:
            phase_match = re.search(
                rf"\*\*\* {phase} \*\*\*(.*?)(?=\*\*\*|$)", hand, re.S
            )

            if phase_match:
                actions = phase_match.group(1).strip()
                cards_match = re.search(
                    rf"\*\*\* {phase} \*\*\* ((?:\[[^\]]+\]\s*)+)", hand
                )
                if cards_match:
                    cards = re.findall(r"\[([^\]]+)\]", cards_match.group(1))
                    cards = " ".join(cards).split()
                else:
                    cards = []

                for action_match in re.finditer(pattern, actions):
                    action = action_match.group("action")
                    action_name = {
                        "raises": "raise",
                        "calls": "call",
                        "folds": "fold",
                        "checks": "check",
                        "bets": "bet",
                    }.get(action, "unknown")

                    amount = (
                        float(action_match.group("amount2"))
                        if action_match.group("amount2")
                        else float(action_match.group("amount1"))
                        if action_match.group("amount1")
                        else None
                    )
                    parsed_action = {
                        "phase": "PRE-FLOP" if phase == "HOLE CARDS" else phase,
                        "player": action_match.group("player"),
                        "action": action_name,
                        "amount": amount,
                        "cards": cards,
                    }
                    print(f"ACTION: {parsed_action}")
                    result.append(parsed_action)

        return result

    def extract_summary(self, hand: str, game_type: str, hero: str):
        patterns = {
            "zoom": {
                "player": r"Seat (?P<seat>\d+): (?P<name>\S+) (.*?\((?P<currency>[^\d\s]+)(?P<amount>[\d\.]+) in chips\))?(?P<details>.*)",
                "pot_and_rake": r"Total pot (?P<currency>[^\d\s]+)(?P<pot>[\d\.]+) \| Rake (?P=currency)(?P<rake>[\d\.]+)",
                "winner_no_showdown": r"Seat (?P<seat>\d+): (?P<name>[^\s\(\)]+)(?: \([^)]+\))? collected \((?P<currency>[^\d\s]+)(?P<amount>[\d\.]+)\)",
                "winner_showdown": r"Seat (?P<seat>\d+): (?P<name>[^\s\(\)]+)(?: \([^)]+\))? showed \[(?P<cards>[^\]]+)\] and won \((?P<currency>[^\d\s]+)(?P<amount>[\d\.]+)\)",
                "looser_shown": r"Seat (?P<seat>\d+): (?P<name>[^\s\(\)]+)(?: \([^)]+\))? muestra \[(?P<cards>[^\]]+)\] y perdió .*",
                "looser_discarded": r"Seat (?P<seat>\d+): (?P<name>[^\s\(\)]+)(?: \([^)]+\))? mucked \[(?P<cards>[^\]]+)\]",
                "community_cards": r"Board \[(?P<cards>[^\]]+)\]",
                "hero_fold": rf"Seat (?P<seat>\d+): {hero}(?: \([^)]+\))? folded (?:before (?P<phase_preflop>Flop)|on the (?P<phase_postflop>\w+))",
            },
            "regular": {
                "player": r"Seat (?P<seat>\d+): (?P<name>\S+) (.*?\((?P<currency>[^\d\s]+)(?P<amount>[\d\.]+) in chips\))?(?P<details>.*)",
                "pot_and_rake": r"Total pot (?P<currency>[^\d\s]+)(?P<pot>[\d\.]+) \| Rake (?P=currency)(?P<rake>[\d\.]+)",
                "winner_no_showdown": r"Seat (?P<seat>\d+): (?P<name>[^\s\(\)]+)(?: \([^)]+\))? collected \((?P<currency>[^\d\s]+)(?P<amount>[\d\.]+)\)",
                "winner_showdown": r"Seat (?P<seat>\d+): (?P<name>[^\s\(\)]+)(?: \([^)]+\))? showed \[(?P<cards>[^\]]+)\] and won \((?P<currency>[^\d\s]+)(?P<amount>[\d\.]+)\)",
                "looser_shown": r"Seat (?P<seat>\d+): (?P<name>[^\s\(\)]+)(?: \([^)]+\))? muestra \[(?P<cards>[^\]]+)\] y perdió .*",
                "looser_discarded": r"Seat (?P<seat>\d+): (?P<name>[^\s\(\)]+)(?: \([^)]+\))? mucked \[(?P<cards>[^\]]+)\]",
                "community_cards": r"Board \[(?P<cards>[^\]]+)\]",
                "hero_fold": rf"Seat (?P<seat>\d+): {hero}(?: \([^)]+\))? folded (?:before (?P<phase_preflop>Flop)|on the (?P<phase_postflop>\w+))",
            },
        }

        pattern = patterns[game_type]
        summary_match = re.search(r"\*\*\* SUMMARY \*\*\*(.*?)(?=\*\*\*|$)", hand, re.S)

        if not summary_match:
            raise Exception("Incorrect SUMMARY format or pattern")

        summary = summary_match.group(1).strip()
        players_actions = []

        for match in re.finditer(pattern["player"], summary):
            player_name = match.group("name")
            player_seat = int(match.group("seat"))
            if player_name == hero:
                hero_seat = player_seat
            players_actions.append(
                {
                    "seat": player_seat,
                    "name": player_name,
                    "details": match.group("details").strip(),
                }
            )

        pot_match = re.search(pattern["pot_and_rake"], summary)
        winner_match = re.search(pattern["winner_no_showdown"], summary)
        showdown = False

        if not winner_match:
            winner_match = re.search(pattern["winner_showdown"], summary)
            showdown = True if winner_match else False

        winner = None
        if winner_match:
            winner = {
                "name": winner_match.group("name"),
                "seat": int(winner_match.group("seat")),
                "cards": winner_match.group("cards").split(" ")
                if "cards" in winner_match.groupdict() and winner_match.group("cards")
                else [],
                "amount": float(winner_match.group("amount")),
            }

        looser = None
        looser_match = re.search(pattern["looser_shown"], summary)
        if not looser_match:
            looser_match = re.search(pattern["looser_discarded"], summary)

        if looser_match:
            looser = {
                "name": looser_match.group("name"),
                "seat": int(looser_match.group("seat")),
                "cards": looser_match.group("cards").split(" "),
            }

        community_cards_match = re.search(pattern["community_cards"], summary)
        community_cards = (
            community_cards_match.group("cards").split(" ")
            if community_cards_match
            else []
        )

        hero_fold_match = re.search(pattern["hero_fold"], summary)
        last_phase_hero_folded = None
        if hero_fold_match:
            if hero_fold_match.group("phase_preflop"):
                last_phase_hero_folded = "PRE_FLOP"
            elif hero_fold_match.group("phase_postflop"):
                last_phase_hero_folded = hero_fold_match.group("phase_postflop").upper()

        return {
            "player_actions": players_actions,
            "pot": float(pot_match.group("pot")) if pot_match else 0,
            "rake": float(pot_match.group("rake")) if pot_match else 0,
            "winner": winner,
            "looser": looser,
            "community_cards": community_cards,
            "showdown": showdown,
            "last_phase_hero_folded": last_phase_hero_folded,
            "hero_seat": hero_seat,
        }

    def extract_showdown(self, hand: str, game_type: str):
        result = {}
        patterns = {
            "zoom": {
                "winner": r"(?P<player>\S+): shows \[(?P<hand>.*?)\] \((?P<description>.*?)\)",
                "looser": r"(?P<player>\S+): mucks hand",
                "collect": r"(?P<player>\S+) collected (?P<amount>[\d\.]+) (?P<currency>[^\d\s]+) from pot",
            },
            "regular": {
                "winner": r"(?P<player>\S+): shows \[(?P<hand>.*?)\] \((?P<description>.*?)\)",
                "looser": r"(?P<player>\S+): mucks hand",
                "collect": r"(?P<player>\S+) collected (?P<amount>[\d\.]+) (?P<currency>[^\d\s]+) from pot",
            },
            "tournament": {
                "winner": r"",
                "looser": r"",
                "collect": r"",
            },
            "sng": {
                "winner": r"",
                "looser": r"",
                "collect": r"",
            },
        }

        pattern = patterns[game_type]

        showdown_section = re.search(
            r"\*\*\* SHOW DOWN \*\*\*(.*?)(?=\*\*\*|$)", hand, re.S
        )
        if not showdown_section:
            return None

        showdown_text = showdown_section.group(1).strip()

        winner_match = re.finditer(pattern["winner"], showdown_text)
        for winner in winner_match:
            if "winner" not in result:
                result["winner"] = []
            result["winner"].append(
                {
                    "player": winner.group("player"),
                    "hand": winner.group("hand").split(),
                    "hand_description": winner.group("description"),
                }
            )

        looser_match = re.finditer(pattern["looser"], showdown_text)
        for looser in looser_match:
            if "looser" not in result:
                result["looser"] = []
            result["looser"].append(looser.group("player"))
            result["looser_action"] = "muck"

        collect_match = re.finditer(pattern["collect"], showdown_text)
        for collect in collect_match:
            if "collector" not in result:
                result["collector"] = []
            result["collector"].append(
                {
                    "player": collect.group("player"),
                    "amount": float(collect.group("amount")),
                    "currency": collect.group("currency"),
                }
            )

        return result

    def extract_finish_before_showdown(self, hand: str, game_type: str):
        result = []
        patterns = {
            "zoom": {
                "uncalled": r"Uncalled bet \((?P<currency>[^\d\s]+)(?P<amount>[\d\.]+)\) returned to (?P<player>\S+)",
                "winner": r"(?P<player>\S+) collected (?P<currency>[^\d\s]+)(?P<amount>[\d\.]+) from pot",
            },
            "regular": {
                "uncalled": r"Uncalled bet \((?P<currency>[^\d\s]+)(?P<amount>[\d\.]+)\) returned to (?P<player>\S+)",
                "winner": r"(?P<player>\S+) collected (?P<currency>[^\d\s]+)(?P<amount>[\d\.]+) from pot",
            },
            "tournament": {
                "uncalled": r"",
                "winner": r"",
            },
            "sng": {
                "uncalled": r"",
                "winner": r"",
            },
        }

        pattern = patterns[game_type]

        uncalled_match = re.search(pattern["uncalled"], hand)
        if uncalled_match:
            uncalled_amount = float(uncalled_match.group("amount"))
            player = uncalled_match.group("player")
            result.append(
                {
                    "player": player,
                    "action": "uncalled_bet_return",
                    "amount": uncalled_amount,
                }
            )

        winner_match = re.search(pattern["winner"], hand)
        if winner_match:
            player = winner_match.group("player")
            amount_won = float(winner_match.group("amount"))
            result.append(
                {
                    "player": player,
                    "action": "wins_pot",
                    "amount": amount_won,
                }
            )

        return result

    def game_type_extractor(self, hand: str):
        is_zoom = re.search("Zoom", hand)
        return "zoom" if is_zoom else "regular"
