from app.history_parser.poker_stars.poker_stars_parser_factory import PokerStarsParserFactory
from app.domain.poker_rooms import PokerRoom
from app.domain.languages import Language
import re

class UnsupportedLanguageError(Exception):
    """Custom exception for unsupported languages."""
    pass
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
        if re.search(r"Asiento", self.transcription) and re.search(r"Mano", self.transcription):
            return Language.SP.value
    
        elif re.search(r"Seat", self.transcription) and re.search(r"Hand", self.transcription):
            return Language.EN.value
    
        else:
            raise UnsupportedLanguageError(f"Not supported language, the available languagues are: {Language.EN.value}, {Language.SP.value}")
    
    def instance_parser(self):
        if self.room == PokerRoom.STARS.value:
            return PokerStarsParserFactory(self.transcription, self.langugage)

        print("Not supported room")
        return None
    
    def parse(self):
        return self.parser.parse()