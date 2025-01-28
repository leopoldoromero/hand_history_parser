from app.history_parser.poker_stars.poker_stars_sp_parser import PokerStarsSpanishParser
from app.history_parser.poker_stars.poker_stars_en_parser import PokerStarsEnglishParser
from app.domain.languages import Language

class PokerStarsParserFactory:
    def __init__(self, transcription: str, language: str):
        self.transcription = transcription
        self.language = language

    def parser_by_language(self):
        return PokerStarsSpanishParser(self.transcription) if self.language == Language.SP.value else PokerStarsEnglishParser(self.transcription)
    
    def parse(self):
        parser = self.parser_by_language()
        return parser.parse()
