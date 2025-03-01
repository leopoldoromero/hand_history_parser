from app.history_parser.history_parser import HistoryParser

spanish_transcription = """
*********** n. 27 **************
Mano n.º 254717173764 de Zoom de PokerStars:  Hold'em No Limit (0.02 €/0.05 €) - 05-02-2025 12:34:49 CET [05-02-2025 6:34:49 ET]
Mesa "Asterope" 6-max El asiento n.º 1 es el botón
Asiento 1: Nicoromero87 (6 € en fichas)
Asiento 2: camamo26 (6.22 € en fichas)
Asiento 3: GhostGambler1 (5.76 € en fichas)
Asiento 4: Mauuu_bg (4.36 € en fichas)
Asiento 5: fraanespinosa (6.49 € en fichas)
camamo26: pone la ciega pequeña 0.02 €
GhostGambler1: pone la ciega grande 0.05 €
*** CARTAS DE MANO ***
Repartidas a Nicoromero87 [Ts 3s]
Mauuu_bg: sube 0.07 € a 0.12 €
fraanespinosa: iguala 0.12 €
Nicoromero87: se retira
camamo26: se retira
GhostGambler1: se retira
*** FLOP *** [6s Th Qd]
Mauuu_bg: apuesta 0.10 €
fraanespinosa: iguala 0.10 €
*** TURN *** [6s Th Qd] [4h]
Mauuu_bg: apuesta 0.16 €
fraanespinosa: iguala 0.16 €
*** RIVER *** [6s Th Qd 4h] [Ac]
Mauuu_bg: pasa
fraanespinosa: pasa
*** SHOW DOWN ***
Mauuu_bg: muestra [Jd Qc] (pareja de damas)
fraanespinosa: descarta su mano sin mostrar
Mauuu_bg se lleva 0.79 € del bote
*** RESUMEN ***
Bote total 0.83 € | Comisión 0.04 €
Comunitarias [6s Th Qd 4h Ac]
Asiento 1: Nicoromero87 (botón) se retiró antes del Flop (no apostó)
Asiento 2: camamo26 (ciega pequeña) se retiró antes del Flop
Asiento 3: GhostGambler1 (ciega grande) se retiró antes del Flop
Asiento 4: Mauuu_bg muestra [Jd Qc] y ganó (0.79 €) con pareja de damas
Asiento 5: fraanespinosa descartó sin mostrar [9h Ks]
"""


def stars_sp_test_parse_players():
    expected_players_response = [
        {"seat": 1, "name": "Nicoromero87", "stack": 6},
        {"seat": 2, "name": "camamo26", "stack": 6.22},
        {"seat": 3, "name": "GhostGambler1", "stack": 5.76},
        {"seat": 4, "name": "Mauuu_bg", "stack": 4.36},
        {"seat": 5, "name": "fraanespinosa", "stack": 6.49},
    ]
    parser = HistoryParser(spanish_transcription)
    parsed_content = parser.parse()
    players = parsed_content[0]["players"]
    for index, player in enumerate(players):
        expected_player = expected_players_response[index]
        assert expected_player["seat"] == player["seat"]
        assert expected_player["name"] == player["name"]
        assert expected_player["stack"] == player["stack"]


def stars_sp_test_parse_actions():
    expected_actions_response = [
        {
            "phase": "PRE-FLOP",
            "player": "Mauuu_bg",
            "action": "raise",
            "amount": 0.12,
            "cards": [],
        },
        {
            "phase": "PRE-FLOP",
            "player": "fraanespinosa",
            "action": "call",
            "amount": 0.12,
            "cards": [],
        },
        {
            "phase": "PRE-FLOP",
            "player": "Nicoromero87",
            "action": "fold",
            "amount": None,
            "cards": [],
        },
        {
            "phase": "PRE-FLOP",
            "player": "camamo26",
            "action": "fold",
            "amount": None,
            "cards": [],
        },
        {
            "phase": "PRE-FLOP",
            "player": "GhostGambler1",
            "action": "fold",
            "amount": None,
            "cards": [],
        },
        {
            "phase": "FLOP",
            "player": "Mauuu_bg",
            "action": "bet",
            "amount": 0.1,
            "cards": ["6s", "Th", "Qd"],
        },
        {
            "phase": "FLOP",
            "player": "fraanespinosa",
            "action": "call",
            "amount": 0.1,
            "cards": ["6s", "Th", "Qd"],
        },
        {
            "phase": "TURN",
            "player": "Mauuu_bg",
            "action": "bet",
            "amount": 0.16,
            "cards": ["6s", "Th", "Qd", "4h"],
        },
        {
            "phase": "TURN",
            "player": "fraanespinosa",
            "action": "call",
            "amount": 0.16,
            "cards": ["6s", "Th", "Qd", "4h"],
        },
        {
            "phase": "RIVER",
            "player": "Mauuu_bg",
            "action": "check",
            "amount": None,
            "cards": ["6s", "Th", "Qd", "4h", "Ac"],
        },
        {
            "phase": "RIVER",
            "player": "fraanespinosa",
            "action": "check",
            "amount": None,
            "cards": ["6s", "Th", "Qd", "4h", "Ac"],
        },
    ]
    parser = HistoryParser(spanish_transcription)
    parsed_content = parser.parse()
    actions = parsed_content[0]["actions"]
    for index, action in enumerate(actions):
        expected_action = expected_actions_response[index]
        assert expected_action["phase"] == action["phase"]
        assert expected_action["player"] == action["player"]
        assert expected_action["action"] == action["action"]
        assert expected_action["amount"] == action["amount"]
        assert expected_action["cards"] == action["cards"]


def stars_sp_test_parse_table_and_btn_info():
    expected_table_name = "Asterope"
    expected_table_type = "6-max"
    expected_btn_seat = 1

    parser = HistoryParser(spanish_transcription)
    parsed_content = parser.parse()

    assert expected_table_name == parsed_content[0]["table_name"]
    assert expected_table_type == parsed_content[0]["table_type"]
    assert expected_btn_seat == parsed_content[0]["button_seat"]


def stars_sp_test_parse_hero_name_hand_and_seat():
    expected_hero_name = "Nicoromero87"
    expected_hero_hand = ["Ts3s"]
    expected_hero_seat = 1

    parser = HistoryParser(spanish_transcription)
    parsed_content = parser.parse()
    hero_name = parsed_content[0]["hero_name"]
    hero_cards = parsed_content[0]["hero_cards"]
    hero_seat = parsed_content[0]["summary"]["hero_seat"]

    assert expected_hero_name == hero_name
    assert expected_hero_hand == hero_cards
    assert expected_hero_seat == hero_seat


def stars_sp_test_parse_summary():
    expected_winner_data = {
        "name": "Mauuu_bg",
        "seat": 4,
        "cards": ["Jd", "Qc"],
        "amount": 0.79,
    }
    expected_looser_data = {"name": "fraanespinosa", "seat": 5, "cards": ["9h", "Ks"]}
    expected_last_phase_hero_folded = "PRE_FLOP"
    expected_hero_seat = 1
    expected_showdown = True
    expected_pot = 0.83
    expected_rake = 0.04

    parser = HistoryParser(spanish_transcription)
    parsed_content = parser.parse()
    winner = parsed_content[0]["summary"]["winner"]
    looser = parsed_content[0]["summary"]["winner"]
    pot = parsed_content[0]["summary"]["pot"]
    rake = parsed_content[0]["summary"]["rake"]
    showdown = parsed_content[0]["summary"]["showdown"]
    last_phase_hero_folded = parsed_content[0]["summary"]["last_phase_hero_folded"]
    hero_seat = parsed_content[0]["summary"]["hero_seat"]

    for key, val in winner.items():
        assert expected_winner_data[key] == val

    for key, val in looser.items():
        assert expected_looser_data[key] == val

    assert expected_pot == pot
    assert expected_rake == rake
    assert expected_showdown == showdown
    assert expected_last_phase_hero_folded == last_phase_hero_folded
    assert expected_hero_seat == hero_seat
