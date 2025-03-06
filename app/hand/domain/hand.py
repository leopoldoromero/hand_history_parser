from typing import List, Optional


class Hero:
    def __init__(self, nick: str, cards: List[str], seat: int):
        self.nick = nick
        self.cards = cards
        self.seat = seat

    @staticmethod
    def from_primitives(data):
        return Hero(nick=data["nick"], cards=data["cards"], seat=data["seat"])

    def to_primitives(self):
        return {"nick": self.nick, "cards": self.cards, "seat": self.seat}


class Player:
    def __init__(self, seat: int, name: str, stack: float):
        self.seat = seat
        self.name = name
        self.stack = stack

    @staticmethod
    def from_primitives(data):
        return Player(seat=data["seat"], name=data["name"], stack=data["stack"])

    def to_primitives(self):
        return {"seat": self.seat, "name": self.name, "stack": self.stack}


class Action:
    def __init__(
        self,
        phase: str,
        player: str,
        action: str,
        amount: Optional[float],
        cards: List[str],
    ):
        self.phase = phase
        self.player = player
        self.action = action
        self.amount = amount
        self.cards = cards

    @staticmethod
    def from_primitives(data):
        return Action(
            phase=data["phase"],
            player=data["player"],
            action=data["action"],
            amount=data.get("amount"),
            cards=data["cards"],
        )

    def to_primitives(self):
        return {
            "phase": self.phase,
            "player": self.player,
            "action": self.action,
            "amount": self.amount,
            "cards": self.cards,
        }


class GeneralInfo:
    def __init__(
        self,
        room_hand_id: str,
        datetime: str,
        game_type: str,
        currency: str,
        small_blind: float,
        big_blind: float,
        game: str,
        room: str,
    ):
        self.room_hand_id = room_hand_id
        self.datetime = datetime
        self.game_type = game_type
        self.currency = currency
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.game = game
        self.room = room

    @staticmethod
    def from_primitives(data):
        return GeneralInfo(
            room_hand_id=data["room_hand_id"],
            datetime=data["datetime"],
            game_type=data["game_type"],
            currency=data["currency"],
            small_blind=data["small_blind"],
            big_blind=data["big_blind"],
            game=data["game"],
            room=data["room"],
        )

    def to_primitives(self):
        return {
            "room_hand_id": self.room_hand_id,
            "datetime": self.datetime,
            "game_type": self.game_type,
            "currency": self.currency,
            "small_blind": self.small_blind,
            "big_blind": self.big_blind,
            "game": self.game,
            "room": self.room,
        }


class SummaryPlayerResult:
    def __init__(
        self,
        seat: int,
        name: str,
        cards: list,
        amount: Optional[float],
    ):
        self.seat = seat
        self.name = name
        self.cards = cards
        self.amount = amount

    @staticmethod
    def from_primitives(data):
        return SummaryPlayerResult(
            seat=data["seat"],
            name=data["name"],
            cards=data["cards"],
            amount=data.get("amount"),
        )

    def to_primitives(self):
        return {
            "seat": self.seat,
            "name": self.name,
            "cards": self.cards,
            "amount": self.amount,
        }


class Summary:
    def __init__(
        self,
        pot: float,
        rake: float,
        winner: SummaryPlayerResult,
        looser: Optional[SummaryPlayerResult],
        community_cards: List[str],
        showdown: bool,
        pot_type: str,
        last_phase_hero_folded: str,
        hero_seat: int,
    ):
        self.pot = pot
        self.rake = rake
        self.winner = winner
        self.looser = looser
        self.community_cards = community_cards
        self.showdown = showdown
        self.pot_type = pot_type
        self.last_phase_hero_folded = last_phase_hero_folded
        self.hero_seat = hero_seat

    @staticmethod
    def from_primitives(data):
        return Summary(
            pot=data["pot"],
            rake=data["rake"],
            winner=SummaryPlayerResult.from_primitives(data["winner"]),
            looser=SummaryPlayerResult.from_primitives(data["looser"])
            if data["looser"]
            else None,
            community_cards=data["community_cards"],
            showdown=data["showdown"],
            pot_type=data["pot_type"],
            last_phase_hero_folded=data["last_phase_hero_folded"],
            hero_seat=data["hero_seat"],
        )

    def to_primitives(self):
        return {
            "pot": self.pot,
            "rake": self.rake,
            "winner": self.winner.to_primitives()
            if self.winner
            else None,  # Include winner field
            "looser": self.looser.to_primitives()
            if self.looser
            else None,  # Include looser field
            "community_cards": self.community_cards,
            "showdown": self.showdown,
            "pot_type": self.pot_type,
            "last_phase_hero_folded": self.last_phase_hero_folded,
            "hero_seat": self.hero_seat,
        }


class Hand:
    def __init__(
        self,
        id: str,
        user_id: str,
        general_info: GeneralInfo,
        table_name: str,
        table_type: str,
        button_seat: int,
        players: List[Player],
        hero_cards: List[str],
        hero_name: str,
        hero_seat: int,
        actions: List[Action],
        summary: Summary,
    ):
        self.id = id
        self.user_id = user_id
        self.general_info = general_info
        self.table_name = table_name
        self.table_type = table_type
        self.button_seat = button_seat
        self.players = players
        self.hero_cards = hero_cards
        self.hero_name = hero_name
        self.hero_seat = hero_seat
        self.actions = actions
        self.summary = summary

    @staticmethod
    def from_primitives(data):
        print("PRIMITIVEs", data.general_info)
        try:
            return Hand(
                id=data["id"],
                user_id=data["user_id"],
                general_info=GeneralInfo.from_primitives(data["general_info"]),
                table_name=data["table_name"],
                table_type=data["table_type"],
                button_seat=data["button_seat"],
                players=[Player.from_primitives(p) for p in data["players"]],
                hero_cards=data["hero_cards"],
                hero_name=data["hero_name"],
                hero_seat=data["hero_seat"],
                actions=[Action.from_primitives(a) for a in data["actions"]],
                summary=Summary.from_primitives(data["summary"]),
            )
        except KeyError as e:
            print(f"Missing key in data: {e}")
            raise
        except Exception as e:
            print(f"Error creating Hand from primitives: {e}")
            raise

    def to_primitives(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "general_info": self.general_info.to_primitives(),
            "table_name": self.table_name,
            "table_type": self.table_type,
            "button_seat": self.button_seat,
            "players": [p.to_primitives() for p in self.players],
            "hero_cards": self.hero_cards,
            "hero_name": self.hero_name,
            "hero_seat": self.hero_seat,
            "actions": [a.to_primitives() for a in self.actions],
            "summary": self.summary.to_primitives(),
        }
