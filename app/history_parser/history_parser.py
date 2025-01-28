from app.history_parser.poker_stars.poker_stars_parser_factory import PokerStarsParserFactory
from app.domain.poker_rooms import PokerRoom
from app.domain.languages import Language

class HistoryParser:
    def __init__(self, transcription: str):
        self.create(transcription)

    def create(self, trasncription: str):
        self.transcription = trasncription
        self.langugage = self.define_language()
        self.room = self.define_room()
        self.parser = self.instance_parser()

    def define_room(self):
        return PokerRoom.STARS.value
    
    def define_language(self):
        return Language.SP.value
    
    def instance_parser(self):
        if self.room == PokerRoom.STARS.value:
            return PokerStarsParserFactory(self.transcription, self.langugage)

        print("Not supported room")
        return None
    
    def parse(self):
        return self.parser.parse()