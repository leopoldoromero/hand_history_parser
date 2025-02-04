import re
from app.domain.poker_rooms import PokerRoom

class PokerStarsSpanishParser:
  def __init__(self, transcription: str):
    self.transcription = transcription

  def parse(self):
    hands = re.split(r"\*{10,}\s*n\.\s*\d+\s*\*{10,}", self.transcription)
    parsed_hands = []
    game_type = self.game_type_extractor(self.transcription)

    for hand in hands:
        if not hand.strip():
            continue
        header_info = self.extract_header_info(hand, game_type)
        players = self.extract_players(hand, game_type)
        hero_hand = self.extract_hero_hand(hand, game_type)
        actions = self.extract_actions(hand, game_type)
        summary = self.extract_summary(hand, game_type)
        showdown = self.extract_showdown(hand, game_type)
        finish_before_showdown = self.extract_finish_before_showdown(hand, game_type)
        
        parsed_hands.append({
          "general_info": header_info,
          "players": players,
          "hero_hand": hero_hand,
          "actions": actions,
          "summary": summary,
          "showdown": showdown,
          "finish_before_showdown": finish_before_showdown
        })
    return parsed_hands
  
  def extract_header_info(self, hand: str, game_type: str):
    patterns = {
      "zoom": r"Mano n.º (?P<hand_id>\d+) de Zoom de PokerStars:.*?((?P<blinds>.+?)) - (?P<datetime>\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}) CET",
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
            "room": PokerRoom.STARS.value
          }

    return None

  def extract_players(self, hand: str, game_type: str):
    players = []
    patterns = {
            "zoom": r'Asiento (?P<seat>\d+): (?P<name>\S+) \((?P<stack>[\d\.]+).*?\)',
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

  def extract_hero_hand(self, hand: str, game_type: str):
    hero_name = "Nicoromero87"
    patterns = {
            "zoom": rf'Repartidas a {re.escape(hero_name)} \[(.*?)\]',
            "regular": r"",
            "tournament": r"",
            "sng": r"",
        }


    if not hand.strip():
      return None

    pattern = patterns[game_type]
    hero_hand_match = re.search(pattern, hand)
    if hero_hand_match:
        return hero_hand_match.group(1).split() 

    return None

  def extract_blinds_actions(self, hand: str, game_type: str):
    result = []
    patterns = {
      "zoom": r"(?P<player>\S+): pone la ciega (?P<type>pequeña|grande) (?P<amount>[\d\.]+)",
      "regular": r"",
      "tournament": r"",
      "sng": r"",
    }
    pattern = patterns[game_type]

    for blind_match in re.finditer(pattern, hand):
      blind_type = {
        "pequeña": "small_blind",
        "grande": "big_blind"
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
    action_phases = ["CARTAS DE MANO", "FLOP", "TURN", "RIVER"]
    patterns = {
      "zoom": r"(?P<player>\S+): (?P<action>sube|iguala|se retira|pasa|apuesta)(?: (?P<amount1>[\d\.]+)(?:\s*[^\d\s])?(?: a (?P<amount2>[\d\.]+)(?:\s*[^\d\s])?)?)?",
      "regular": r"",
      "tournament": r"",
      "sng": r"",
    }

    pattern = patterns[game_type]

    if not hand.strip():
      return None

    board_cards = []

    for phase in action_phases:
      phase_match = re.search(rf"\*\*\* {phase} \*\*\*(.*?)(?=\*\*\*|$)", hand, re.S)
            
      if phase_match:
        actions = phase_match.group(1).strip()
        cards_match = re.findall(r"\[(.*?)\]", phase_match.group(0).strip())  
        if cards_match and phase != "CARTAS DE MANO":
          new_cards = " ".join(cards_match).split()  
          board_cards = list(dict.fromkeys(board_cards + new_cards)) 

        for action_match in re.finditer(pattern, actions):
          action = action_match.group("action")
          action_name = {
            "sube": "raise",
            "iguala": "call",
            "se retira": "fold",
            "pasa": "check",
            "apuesta": "bet",
          }.get(action, "unknown")

          
          amount = (
            float(action_match.group("amount2"))
            if action_match.group("amount2")
            else float(action_match.group("amount1"))
            if action_match.group("amount1")
            else None
          )

          result.append({
            "phase": "PRE-FLOP" if phase == "CARTAS DE MANO" else phase,
            "player": action_match.group("player"),
            "action": action_name,
            "amount": amount,
            "cards": board_cards[:]
          })

    return result

  def extract_summary(self, hand: str, game_type: str):
    players_actions = []
    patterns = {
      "zoom": {
        "player": r"Asiento (?P<seat>\d+): (?P<name>\S+) (.*?\((?P<amount>[\d\.]+)\s*\S*\))?",
        "pot_and_rake": r"Bote total\s+(?P<pot>[\d\.]+)\s*\S*\s*\|\s*Comisión\s+(?P<rake>[\d\.]+)\s*\S*"
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
    summary_match = re.search(r"\*\*\* RESUMEN \*\*\*(.*?)(?=\*\*\*|$)", hand, re.S)
    if summary_match:
      summary = summary_match.group(1).strip()
      for summary_action_match in re.finditer(pattern["player"], summary):
        players_actions.append({
          "seat": int(summary_action_match.group("seat")),
          "name": summary_action_match.group("name"),
          "details": summary_action_match.group(3) if summary_action_match.group(3) else "",
          "amount": float(summary_action_match.group("amount")) if summary_action_match.group("amount") else 0,
        })
      pot_match = re.search(pattern["pot_and_rake"], summary)
      pot = float(pot_match.group("pot")) if pot_match.group("pot") else 0
      rake = float(pot_match.group("rake")) if pot_match.group("rake") else 0
      return {
          "player_actions": players_actions,
          "pot": pot,
          "rake": rake
      }
  
  def extract_showdown(self, hand: str, game_type: str):
    result = {}
    patterns = {
      "zoom": {
        "winner": r"(?P<player>\S+): muestra \[(?P<hand>.*?)\] \((?P<description>.*?)\)",
        "loser": r"(?P<player>\S+): descarta su mano sin mostrar"
      },
      "regular": {
        "winner": r"",
        "loser": r"",
      },
      "tournament": {
        "winner": r"",
        "loser": r"",
      },
      "sng": {
        "winner": r"",
        "loser": r"",
      },
    }

    pattern = patterns[game_type]

    showdown_section = re.search(r"\*\*\* SHOW DOWN \*\*\*(.*?)(?=\*\*\*|$)", hand, re.S)
    if not showdown_section:
      return None

    showdown_text = showdown_section.group(1).strip()

    winner_match = re.search(pattern["winner"], showdown_text)
    if winner_match:
      result["winner"] = winner_match.group("player")
      result["winner_hand"] = winner_match.group("hand").split()
      result["winner_hand_description"] = winner_match.group("description")

    loser_match = re.search(pattern["loser"], showdown_text)
    if loser_match:
      result["loser"] = loser_match.group("player")
      result["loser_action"] = "muck"  

    return result
  
  def extract_finish_before_showdown(self, hand: str, game_type: str):
    result = []
    patterns = {
      "zoom": {
        "uncalled": r"La apuesta no igualada \(([\d\.]+)\s*\S*\) ha sido devuelta a (\S+)",
        "winner": r"(\S+) se lleva ([\d\.]+) € del bote"
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
      uncalled_amount = float(uncalled_match.group(1))
      player = uncalled_match.group(2)
      result.append({
        "player": player,
        "action": "uncalled_bet_return",
        "amount": uncalled_amount,
      })
    winner_match = re.search(pattern["winner"], hand)
    if winner_match:
      player = winner_match.group(1)
      amount_won = float(winner_match.group(2))
      result.append({
        "player": player,
        "action": "wins_pot",
        "amount": amount_won,
      })
    return result
  
  def game_type_extractor(self, hand: str):
    is_zoom = re.search("Zoom", hand)
    return "zoom" if is_zoom else "regular"

