from app.history_parser.history_parser import HistoryParser

english_transcription = """
*********** # 5 **************
PokerStars Zoom Hand #254755222944:  Hold'em No Limit (€0.02/€0.05) - 2025/02/07 21:46:39 CET [2025/02/07 15:46:39 ET]
Table 'Asterope' 6-max Seat #1 is the button
Seat 1: ascool40 (€5.02 in chips)
Seat 2: Nicoromero87 (€5.93 in chips)
Seat 3: Redbox615 (€5 in chips)
Seat 4: Aless0510 (€4.96 in chips)
Seat 5: MakesMeRich (€5 in chips)
Seat 6: Bustelopower (€4.06 in chips)
Nicoromero87: posts small blind €0.02
Redbox615: posts big blind €0.05
*** HOLE CARDS ***
Dealt to Nicoromero87 [Td 6d]
Aless0510: folds
MakesMeRich: folds
Bustelopower: folds
ascool40: folds
Nicoromero87: raises €0.10 to €0.15
Redbox615: calls €0.10
*** FLOP *** [Jd 6c 4h]
Nicoromero87: checks
Redbox615: bets €0.10
Nicoromero87: calls €0.10
*** TURN *** [Jd 6c 4h] [Th]
Nicoromero87: checks
Redbox615: checks
*** RIVER *** [Jd 6c 4h Th] [8d]
Nicoromero87: checks
Redbox615: checks
*** SHOW DOWN ***
Nicoromero87: shows [Td 6d] (two pair, Tens and Sixes)
Redbox615: mucks hand
Nicoromero87 collected €0.48 from pot
*** SUMMARY ***
Total pot €0.50 | Rake €0.02
Board [Jd 6c 4h Th 8d]
Seat 1: ascool40 (button) folded before Flop (didn't bet)
Seat 2: Nicoromero87 (small blind) showed [Td 6d] and won (€0.48) with two pair, Tens and Sixes
Seat 3: Redbox615 (big blind) mucked [Ad 4c]
Seat 4: Aless0510 folded before Flop (didn't bet)
Seat 5: MakesMeRich folded before Flop (didn't bet)
Seat 6: Bustelopower folded before Flop (didn't bet)
"""


def stars_en_test_parse_players():
    expected_players_response = [
        {"seat": 1, "name": "ascool40", "stack": 5.02},
        {"seat": 2, "name": "Nicoromero87", "stack": 5.93},
        {"seat": 3, "name": "Redbox615", "stack": 5.0},
        {"seat": 4, "name": "Aless0510", "stack": 4.96},
        {"seat": 5, "name": "MakesMeRich", "stack": 5.0},
        {"seat": 6, "name": "Bustelopower", "stack": 4.06},
    ]
    parser = HistoryParser(english_transcription)
    parsed_content = parser.parse()
    players = parsed_content[0]["players"]
    for index, player in enumerate(players):
        expected_player = expected_players_response[index]
        assert expected_player["seat"] == player["seat"]
        assert expected_player["name"] == player["name"]
        assert expected_player["stack"] == player["stack"]


def stars_en_test_parse_actions():
    expected_actions_response = [
        {
            "phase": "PRE-FLOP",
            "player": "Aless0510",
            "action": "fold",
            "amount": None,
            "cards": [],
        },
        {
            "phase": "PRE-FLOP",
            "player": "MakesMeRich",
            "action": "fold",
            "amount": None,
            "cards": [],
        },
        {
            "phase": "PRE-FLOP",
            "player": "Bustelopower",
            "action": "fold",
            "amount": None,
            "cards": [],
        },
        {
            "phase": "PRE-FLOP",
            "player": "ascool40",
            "action": "fold",
            "amount": None,
            "cards": [],
        },
        {
            "phase": "PRE-FLOP",
            "player": "Nicoromero87",
            "action": "raise",
            "amount": 0.15,
            "cards": [],
        },
        {
            "phase": "PRE-FLOP",
            "player": "Redbox615",
            "action": "call",
            "amount": 0.1,
            "cards": [],
        },
        {
            "phase": "FLOP",
            "player": "Nicoromero87",
            "action": "check",
            "amount": None,
            "cards": ["Jd", "6c", "4h"],
        },
        {
            "phase": "FLOP",
            "player": "Redbox615",
            "action": "bet",
            "amount": 0.1,
            "cards": ["Jd", "6c", "4h"],
        },
        {
            "phase": "FLOP",
            "player": "Nicoromero87",
            "action": "call",
            "amount": 0.1,
            "cards": ["Jd", "6c", "4h"],
        },
        {
            "phase": "TURN",
            "player": "Nicoromero87",
            "action": "check",
            "amount": None,
            "cards": ["Jd", "6c", "4h", "Th"],
        },
        {
            "phase": "TURN",
            "player": "Redbox615",
            "action": "check",
            "amount": None,
            "cards": ["Jd", "6c", "4h", "Th"],
        },
        {
            "phase": "RIVER",
            "player": "Nicoromero87",
            "action": "check",
            "amount": None,
            "cards": ["Jd", "6c", "4h", "Th", "8d"],
        },
        {
            "phase": "RIVER",
            "player": "Redbox615",
            "action": "check",
            "amount": None,
            "cards": ["Jd", "6c", "4h", "Th", "8d"],
        },
    ]
    parser = HistoryParser(english_transcription)
    parsed_content = parser.parse()
    actions = parsed_content[0]["actions"]
    for index, action in enumerate(actions):
        expected_action = expected_actions_response[index]
        assert expected_action["phase"] == action["phase"]
        assert expected_action["player"] == action["player"]
        assert expected_action["action"] == action["action"]
        assert expected_action["amount"] == action["amount"]
        assert expected_action["cards"] == action["cards"]


def stars_en_test_parse_table_and_btn_info():
    expected_table_name = "Asterope"
    expected_table_type = "6-max"
    expected_btn_seat = 1

    parser = HistoryParser(english_transcription)
    parsed_content = parser.parse()

    assert expected_table_name == parsed_content[0]["table_name"]
    assert expected_table_type == parsed_content[0]["table_type"]
    assert expected_btn_seat == parsed_content[0]["button_seat"]


def stars_en_test_parse_hero_name_hand_and_seat():
    expected_hero_name = "Nicoromero87"
    expected_hero_hand = ["Td", "6d"]
    expected_hero_seat = 2

    parser = HistoryParser(english_transcription)
    parsed_content = parser.parse()
    hero_name = parsed_content[0]["hero_name"]
    hero_cards = parsed_content[0]["hero_cards"]
    hero_seat = parsed_content[0]["summary"]["hero_seat"]

    assert expected_hero_name == hero_name
    assert expected_hero_hand == hero_cards
    assert expected_hero_seat == hero_seat


def stars_en_test_parse_summary():
    expected_winner_data = {
        "name": "Nicoromero87",
        "seat": 2,
        "cards": ["Td", "6d"],
        "amount": 0.48,
    }
    expected_looser_data = {"name": "Redbox615", "seat": 3, "cards": ["Ad", "4c"]}
    expected_last_phase_hero_folded = None
    expected_showdown = True
    expected_pot = 0.5
    expected_rake = 0.02

    parser = HistoryParser(english_transcription)
    parsed_content = parser.parse()
    winner = parsed_content[0]["summary"]["winner"]
    looser = parsed_content[0]["summary"]["winner"]
    pot = parsed_content[0]["summary"]["pot"]
    rake = parsed_content[0]["summary"]["rake"]
    showdown = parsed_content[0]["summary"]["showdown"]
    last_phase_hero_folded = parsed_content[0]["summary"]["last_phase_hero_folded"]

    for key, val in winner.items():
        assert expected_winner_data[key] == val

    for key, val in looser.items():
        assert expected_looser_data[key] == val

    assert expected_pot == pot
    assert expected_rake == rake
    assert expected_showdown == showdown
    assert expected_last_phase_hero_folded == last_phase_hero_folded
