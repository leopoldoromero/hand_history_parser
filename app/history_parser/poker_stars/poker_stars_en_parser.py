import re

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
        summary = self.extract_summary(hand, game_type)
        showdown = self.extract_showdown(hand, game_type)
        finish_before_showdown = self.extract_finish_before_showdown(hand, game_type)
        parsed_hands.append({
          "general_info": header_info,
          "players": players,
          "hero_cards": hero_hand,
          "hero_name": hero_name,
          "actions": actions,
          "summary": summary,
          "showdown": showdown,
          "finish_before_showdown": finish_before_showdown
        })
    return parsed_hands
  
  def extract_header_info(self, hand: str, game_type: str):
    patterns = {
      "zoom": r"PokerStars Zoom Hand #(?P<hand_id>\d+):.*?\((?P<blinds>.+?)\) - (?P<datetime>\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) CET",
      "regular": r"",
      "tournament": r"",
      "sng": r"",
    }

    if not hand.strip():
      return None

    pattern = patterns[game_type]
    match = re.search(pattern, hand)
    if match:
        hand_id = match.group("hand_id")
        datetime = match.group("datetime")
        blinds = match.group("blinds") if "blinds" in match.groupdict() else None
        currency = "€" if "€" in blinds else "$" if blinds else None
        blinds_match = re.search(r"((?P<small_blind>[\d.]+)[^0-9]+(?P<big_blind>[\d.]+))", blinds)
        if blinds_match:
          blinds = (float(blinds_match.group("small_blind")), float(blinds_match.group("big_blind")))

          return {
            "hand_id": hand_id,
            "datetime": datetime,
            "game_type": game_type,
            "currency": currency,
            "small_blind": blinds[0] if blinds else None,
            "big_blind": blinds[1] if blinds else None,
            "game": "Hold'em",  # Assuming Hold'em for now
          }

    return None

  def extract_players(self, hand: str, game_type: str):
    players = []
    patterns = {
            "zoom": r'Seat (?P<seat>\d+): (?P<name>\S+) \((?P<currency>\S+)(?P<stack>[\d\.]+) in chips\)',
            "regular": r"",
            "tournament": r"",
            "sng": r"",
        }

    if not hand.strip():
      return None

    pattern = patterns[game_type]

    for player_match in re.finditer(pattern, hand):
        
        players.append({
          "seat": int(player_match.group("seat")),
          "name": player_match.group("name"),
          "stack": float(player_match.group("stack")),
        })

    return players

  def extract_hero_info(self, hand: str, game_type: str):
    patterns = {
            "zoom": rf'Dealt to (?P<hero>\S+) \[(.*?)\]',
            "regular": r"",
            "tournament": r"",
            "sng": r"",
        }


    if not hand.strip():
      return None

    pattern = patterns[game_type]
    hero_hand_match = re.search(pattern, hand)
    if hero_hand_match:
        hero_name = hero_hand_match.group("hero")
        hero_hand = hero_hand_match.group(2).split() 
        return hero_name, hero_hand 

    return None

  def extract_blinds_actions(self, hand: str, game_type: str):
    result = []
    patterns = {
      "zoom": r"(?P<player>\S+): posts (?P<type>small|big) blind (?P<currency>[^\d\s]+)(?P<amount>\d+\.\d+)",
      "regular": r"",
      "tournament": r"",
      "sng": r"",
    }
    pattern = patterns[game_type]

    for blind_match in re.finditer(pattern, hand):
      blind_type = {
        "small": "small_blind",
        "big": "big_blind"
      }[blind_match.group("type")]
      amount = float(blind_match.group("amount"))
      result.append({
        "phase": "PRE-FLOP",
        "player": blind_match.group("player"),
        "action": blind_type,
        "amount": amount,
        "cards": [],
      })
    return result 


  def extract_actions(self, hand: str, game_type: str):
    blinds = self.extract_blinds_actions(hand, game_type)
    result = blinds[:]
    action_phases = ["HOLE CARDS", "FLOP", "TURN", "RIVER"]
    patterns = {
      "zoom": r"(?P<player>\S+): (?P<action>raises|calls|folds|checks|bets)(?: (?P<currency>[^\d\s]+)(?P<amount1>[\d\.]+)(?: to (?P=currency)(?P<amount2>[\d\.]+))?)?",
      "regular": r"",
      "tournament": r"",
      "sng": r"",
    }

    pattern = patterns[game_type]

    if not hand.strip():
      return None


    for phase in action_phases:
      phase_match = re.search(rf"\*\*\* {phase} \*\*\*(.*?)(?=\*\*\*|$)", hand, re.S)
            
      if phase_match:
        actions = phase_match.group(1).strip()
        cards_match = re.search(rf"\*\*\* {phase} \*\*\* \[(.*?)\]", hand)
        cards = cards_match.group(1).split() if cards_match else []

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

          result.append({
            "phase": "PRE-FLOP" if phase == "HOLE CARDS" else phase,
            "player": action_match.group("player"),
            "action": action_name,
            "amount": amount,
            "cards": cards
          })

    return result

  def extract_summary(self, hand: str, game_type: str):
    players_actions = []
    patterns = {
        "zoom": {
          "player": r"Seat (?P<seat>\d+): (?P<name>\S+) (.*?\((?P<currency>[^\d\s]+)(?P<amount>[\d\.]+) in chips\))?(?P<details>.*)",
          "pot_and_rake": r"Total pot (?P<currency>[^\d\s]+)(?P<pot>[\d\.]+) \| Rake (?P=currency)(?P<rake>[\d\.]+)"
      },
        "regular": {
          "player": r"",
          "pot_and_rake": r"",
        },
        "tournament": {
          "player": r"",
          "pot_and_rake": r"",
        },
        "sng": {
          "player": r"",
          "pot_and_rake": r"",
        },
      }

    pattern = patterns[game_type]
    summary_match = re.search(r"\*\*\* SUMMARY \*\*\*(.*?)(?=\*\*\*|$)", hand, re.S)
      
    if not summary_match:
      return None

    summary = summary_match.group(1).strip()
    players_actions = []

    for match in re.finditer(pattern["player"], summary):
      players_actions.append({
        "seat": int(match.group("seat")),
        "name": match.group("name"),
        "details": match.group("details").strip() if match.group("details") else "",  # Capture details
        "amount": float(match.group("amount")) if match.group("amount") else 0,
        "currency": match.group("currency") if match.group("amount") else None
      })

    pot_match = re.search(pattern["pot_and_rake"], summary)
      
    return {
      "player_actions": players_actions,
      "pot": float(pot_match.group("pot")) if pot_match else 0,
      "rake": float(pot_match.group("rake")) if pot_match else 0,
      "currency": pot_match.group("currency") if pot_match else None
    }
  
  def extract_showdown(self, hand: str, game_type: str):
    result = {}
    patterns = {
        "zoom": {
            "winner": r"(?P<player>\S+): shows \[(?P<hand>.*?)\] \((?P<description>.*?)\)",
            "loser": r"(?P<player>\S+): mucks hand",
            "collect": r"(?P<player>\S+) collected (?P<amount>[\d\.]+) (?P<currency>[^\d\s]+) from pot"
        },
        "regular": {
            "winner": r"",
            "loser": r"",
            "collect": r"",
        },
        "tournament": {
            "winner": r"",
            "loser": r"",
            "collect": r"",
        },
        "sng": {
            "winner": r"",
            "loser": r"",
            "collect": r"",
        },
    }

    pattern = patterns[game_type]

    showdown_section = re.search(r"\*\*\* SHOW DOWN \*\*\*(.*?)(?=\*\*\*|$)", hand, re.S)
    if not showdown_section:
        return None

    showdown_text = showdown_section.group(1).strip()

    winner_match = re.finditer(pattern["winner"], showdown_text)
    for winner in winner_match:
        if "winner" not in result:
            result["winner"] = []
        result["winner"].append({
            "player": winner.group("player"),
            "hand": winner.group("hand").split(),
            "hand_description": winner.group("description")
        })

    loser_match = re.finditer(pattern["loser"], showdown_text)
    for loser in loser_match:
        if "loser" not in result:
            result["loser"] = []
        result["loser"].append(loser.group("player"))
        result["loser_action"] = "muck"

    collect_match = re.finditer(pattern["collect"], showdown_text)
    for collect in collect_match:
        if "collector" not in result:
            result["collector"] = []
        result["collector"].append({
            "player": collect.group("player"),
            "amount": float(collect.group("amount")),
            "currency": collect.group("currency")
        })

    return result 
  
  def extract_finish_before_showdown(self, hand: str, game_type: str):
    result = []
    patterns = {
        "zoom": {
            "uncalled": r"Uncalled bet \((?P<currency>[^\d\s]+)(?P<amount>[\d\.]+)\) returned to (?P<player>\S+)",
            "winner": r"(?P<player>\S+) collected (?P<currency>[^\d\s]+)(?P<amount>[\d\.]+) from pot"
        },
        "regular": {
            "uncalled": r"",
            "winner": r"",
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
        result.append({
            "player": player,
            "action": "uncalled_bet_return",
            "amount": uncalled_amount,
        })

    winner_match = re.search(pattern["winner"], hand)
    if winner_match:
        player = winner_match.group("player")
        amount_won = float(winner_match.group("amount"))
        result.append({
            "player": player,
            "action": "wins_pot",
            "amount": amount_won,
        })

    return result
  
  def game_type_extractor(self, hand: str):
    is_zoom = re.search("Zoom", hand)
    return "zoom" if is_zoom else "regular"

