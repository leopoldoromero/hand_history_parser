# from app.history_parser.history_parser import HistoryParser

# spanish_transcription = """
# *********** n. 1 **************
# Mano n.º 254718322088 de Zoom de PokerStars:  Hold'em No Limit (0.02 €/0.05 €) - 05-02-2025 14:48:32 CET [05-02-2025 8:48:32 ET]
# Mesa "Asterope" 6-max El asiento n.º 1 es el botón
# Asiento 1: Ermufa (4.59 € en fichas)
# Asiento 2: alfonsoterrible (4.95 € en fichas)
# Asiento 3: otot1302 (4.90 € en fichas)
# Asiento 4: sonieta1991 (4.91 € en fichas)
# Asiento 5: Nicoromero87 (6 € en fichas)
# alfonsoterrible: pone la ciega pequeña 0.02 €
# otot1302: pone la ciega grande 0.05 €
# *** CARTAS DE MANO ***
# Repartidas a Nicoromero87 [8c 9c]
# sonieta1991: se retira
# Nicoromero87 no tiene conexión
# Nicoromero87 ha agotado su tiempo mientras siga sin conexión
# Nicoromero87: se retira
# Ermufa: se retira
# alfonsoterrible: se retira
# La apuesta no igualada (0.03 €) ha sido devuelta a otot1302
# otot1302 se lleva 0.04 € del bote
# otot1302: no muestra su mano
# *** RESUMEN ***
# Bote total 0.04 € | Comisión 0 €
# Asiento 1: Ermufa (botón) se retiró antes del Flop (no apostó)
# Asiento 2: alfonsoterrible (ciega pequeña) se retiró antes del Flop
# Asiento 3: otot1302 (ciega grande) recaudó (0.04 €)
# Asiento 4: sonieta1991 se retiró antes del Flop (no apostó)
# Asiento 5: Nicoromero87 se retiró antes del Flop (no apostó)
# """

# english_transcription = """

# *********** # 5 **************
# PokerStars Zoom Hand #254755222944:  Hold'em No Limit (€0.02/€0.05) - 2025/02/07 21:46:39 CET [2025/02/07 15:46:39 ET]
# Table 'Asterope' 6-max Seat #1 is the button
# Seat 1: ascool40 (€5.02 in chips)
# Seat 2: Nicoromero87 (€5.93 in chips)
# Seat 3: Redbox615 (€5 in chips)
# Seat 4: Aless0510 (€4.96 in chips)
# Seat 5: MakesMeRich (€5 in chips)
# Seat 6: Bustelopower (€4.06 in chips)
# Nicoromero87: posts small blind €0.02
# Redbox615: posts big blind €0.05
# *** HOLE CARDS ***
# Dealt to Nicoromero87 [Td 6d]
# Aless0510: folds
# MakesMeRich: folds
# Bustelopower: folds
# ascool40: folds
# Nicoromero87: raises €0.10 to €0.15
# Redbox615: calls €0.10
# *** FLOP *** [Jd 6c 4h]
# Nicoromero87: checks
# Redbox615: bets €0.10
# Nicoromero87: calls €0.10
# *** TURN *** [Jd 6c 4h] [Th]
# Nicoromero87: checks
# Redbox615: checks
# *** RIVER *** [Jd 6c 4h Th] [8d]
# Nicoromero87: checks
# Redbox615: checks
# *** SHOW DOWN ***
# Nicoromero87: shows [Td 6d] (two pair, Tens and Sixes)
# Redbox615: mucks hand
# Nicoromero87 collected €0.48 from pot
# *** SUMMARY ***
# Total pot €0.50 | Rake €0.02
# Board [Jd 6c 4h Th 8d]
# Seat 1: ascool40 (button) folded before Flop (didn't bet)
# Seat 2: Nicoromero87 (small blind) showed [Td 6d] and won (€0.48) with two pair, Tens and Sixes
# Seat 3: Redbox615 (big blind) mucked [Ad 4c]
# Seat 4: Aless0510 folded before Flop (didn't bet)
# Seat 5: MakesMeRich folded before Flop (didn't bet)
# Seat 6: Bustelopower folded before Flop (didn't bet)
# """


# def test_parse_english_players():
#     expected_players_response = [
#         {"seat": 1, "name": "ascool40", "stack": 5.02},
#         {"seat": 2, "name": "Nicoromero87", "stack": 5.93},
#         {"seat": 3, "name": "Redbox615", "stack": 5.0},
#         {"seat": 4, "name": "Aless0510", "stack": 4.96},
#         {"seat": 5, "name": "MakesMeRich", "stack": 5.0},
#         {"seat": 6, "name": "Bustelopower", "stack": 4.06},
#     ]
#     parser = HistoryParser(english_transcription)
#     parsed_content = parser.parse()
#     players = parsed_content[0]["players"]
#     for index, player in enumerate(players):
#         expected_player = expected_players_response[index]
#         assert expected_player["seat"] == player["seat"]
#         assert expected_player["name"] == player["name"]
#         assert expected_player["stack"] == player["stack"]


# def test_parse_history_spanish():
#     parser = HistoryParser(spanish_transcription)
#     expected_hand_id = "254718322088"
#     expected_table_name = "Asterope"
#     expected_table_type = "6-max"
#     expected_hero_seat = 5
#     expected_hero_name = "Nicoromero87"
#     expected_hero_cards = ["8c", "9c"]
#     expected_actions_len = 6
#     expected_players_len = 5
#     expected_button_seat = 1
#     expected_pot_type = "UNOPENED"

#     parsed_content = parser.parse()
#     hand_id = parsed_content[0]["general_info"]["hand_id"]
#     table_name = parsed_content[0]["table_name"]
#     table_type = parsed_content[0]["table_type"]
#     hero_seat = parsed_content[0]["hero_seat"]
#     hero_name = parsed_content[0]["hero_name"]
#     hero_cards = parsed_content[0]["hero_cards"]
#     players = parsed_content[0]["players"]
#     actions = parsed_content[0]["actions"]
#     button_seat = parsed_content[0]["button_seat"]
#     pot_type = parsed_content[0]["summary"]["pot_type"]

#     assert expected_hand_id == hand_id
#     assert expected_table_name == table_name
#     assert expected_table_type == table_type
#     assert expected_hero_seat == hero_seat
#     assert expected_hero_name == hero_name
#     assert all(
#         expected_hero_cards[index] == value for index, value in enumerate(hero_cards)
#     )
#     assert len(actions) == expected_actions_len
#     assert len(players) == expected_players_len
#     assert expected_button_seat == button_seat
#     assert expected_pot_type == pot_type


# def test_parse_history_english():
#     parser = HistoryParser(english_transcription)
#     expected_hand_id = "254755246480"
#     expected_table_name = "Asterope"
#     expected_table_type = "6-max"
#     expected_hero_seat = 5
#     expected_hero_name = "Nicoromero87"
#     expected_hero_cards = ["7c", "Js"]
#     expected_actions_len = 12
#     expected_players_len = 6
#     expected_button_seat = 1
#     expected_pot_type = "OPEN_RAISED"

#     parsed_content = parser.parse()
#     hand_id = parsed_content[0]["general_info"]["hand_id"]
#     table_name = parsed_content[0]["table_name"]
#     table_type = parsed_content[0]["table_type"]
#     hero_seat = parsed_content[0]["hero_seat"]
#     hero_name = parsed_content[0]["hero_name"]
#     hero_cards = parsed_content[0]["hero_cards"]
#     players = parsed_content[0]["players"]
#     actions = parsed_content[0]["actions"]
#     button_seat = parsed_content[0]["button_seat"]
#     pot_type = parsed_content[0]["summary"]["pot_type"]

#     assert expected_hand_id == hand_id
#     assert expected_table_name == table_name
#     assert expected_table_type == table_type
#     assert expected_hero_seat == hero_seat
#     assert expected_hero_name == hero_name
#     assert all(
#         expected_hero_cards[index] == value for index, value in enumerate(hero_cards)
#     )
#     assert len(actions) == expected_actions_len
#     assert len(players) == expected_players_len
#     assert expected_button_seat == button_seat
#     assert expected_pot_type == pot_type
