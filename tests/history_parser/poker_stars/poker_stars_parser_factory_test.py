from app.history_parser.poker_stars.poker_stars_parser_factory import PokerStarsParserFactory
from app.history_parser.poker_stars.poker_stars_sp_parser import PokerStarsSpanishParser
from app.history_parser.poker_stars.poker_stars_en_parser import PokerStarsEnglishParser
from app.domain.languages import Language

def test_poker_stars_factory_returns_the_right_parser():
    expected_parsers = [PokerStarsSpanishParser, PokerStarsEnglishParser]
    languages = [Language.SP.value, Language.EN.value]
    transcription = ""
    
    for index, language in enumerate(languages):
        parser = PokerStarsParserFactory(transcription, language)
        obtained_instance = parser.parser_by_language()
        expected_parser = expected_parsers[index]
        
        assert isinstance(obtained_instance, expected_parser), f"Parser for languague '{language}' does not match. Expected: {expected_parser}, but got: {obtained_instance.__class__}"

