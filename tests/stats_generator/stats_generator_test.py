from app.stats_generator.game_state_handler import GameStateHandler

mock_hands = [
        {
            "general_info": {
                "hand_id": "254718322088",
                "datetime": "05-02-2025 14:48:32",
                "game_type": "zoom",
                "currency": "€",
                "small_blind": 0.02,
                "big_blind": 0.05,
                "game": "Hold'em",
                "room": "STARS"
            },
            "table_name": "Asterope",
            "table_type": "6-max",
            "button_seat": 1,
            "players": [
                {
                    "seat": 1,
                    "name": "Ermufa",
                    "stack": 4.59
                },
                {
                    "seat": 2,
                    "name": "alfonsoterrible",
                    "stack": 4.95
                },
                {
                    "seat": 3,
                    "name": "otot1302",
                    "stack": 4.9
                },
                {
                    "seat": 4,
                    "name": "sonieta1991",
                    "stack": 4.91
                },
                {
                    "seat": 5,
                    "name": "Nicoromero87",
                    "stack": 6.0
                }
            ],
            "hero_cards": [
                "8c",
                "9c"
            ],
            "hero_name": "Nicoromero87",
            "hero_seat": 5,
            "actions": [
                {
                    "phase": "PRE-FLOP",
                    "player": "alfonsoterrible",
                    "action": "small_blind",
                    "amount": 0.02,
                    "cards": []
                },
                {
                    "phase": "PRE-FLOP",
                    "player": "otot1302",
                    "action": "big_blind",
                    "amount": 0.05,
                    "cards": []
                },
                {
                    "phase": "PRE-FLOP",
                    "player": "sonieta1991",
                    "action": "fold",
                    "amount": None,
                    "cards": []
                },
                {
                    "phase": "PRE-FLOP",
                    "player": "Nicoromero87",
                    "action": "fold",
                    "amount": None,
                    "cards": []
                },
                {
                    "phase": "PRE-FLOP",
                    "player": "Ermufa",
                    "action": "fold",
                    "amount": None,
                    "cards": []
                },
                {
                    "phase": "PRE-FLOP",
                    "player": "alfonsoterrible",
                    "action": "fold",
                    "amount": None,
                    "cards": []
                }
            ],
            "summary": {
                "player_actions": [
                    {
                        "seat": 1,
                        "name": "Ermufa",
                        "details": "se retiró antes del Flop (no apostó)"
                    },
                    {
                        "seat": 2,
                        "name": "alfonsoterrible",
                        "details": "se retiró antes del Flop"
                    },
                    {
                        "seat": 3,
                        "name": "otot1302",
                        "details": "recaudó (0.04 €)"
                    },
                    {
                        "seat": 4,
                        "name": "sonieta1991",
                        "details": "se retiró antes del Flop (no apostó)"
                    },
                    {
                        "seat": 5,
                        "name": "Nicoromero87",
                        "details": "se retiró antes del Flop (no apostó)"
                    }
                ],
                "pot": 0.04,
                "rake": 0.0,
                "currency": "€",
                "winner": {
                    "name": "otot1302",
                    "seat": 3,
                    "cards": [],
                    "amount": 0.04,
                    "currency": "€"
                },
                "looser": None,
                "community_cards": [],
                "showdown": False,
                "last_phase_hero_folded": "PRE_FLOP",
                "hero_seat": 5,
                "pot_type": "UNOPENED"
            },
            "showdown": None,
            "finish_before_showdown": [
                {
                    "player": "otot1302",
                    "action": "uncalled_bet_return",
                    "amount": 0.03
                },
                {
                    "player": "otot1302",
                    "action": "wins_pot",
                    "amount": 0.04
                }
            ]
        },
        {
            "general_info": {
                "hand_id": "254718320478",
                "datetime": "05-02-2025 14:48:23",
                "game_type": "zoom",
                "currency": "€",
                "small_blind": 0.02,
                "big_blind": 0.05,
                "game": "Hold'em",
                "room": "STARS"
            },
            "table_name": "Asterope",
            "table_type": "6-max",
            "button_seat": 1,
            "players": [
                {
                    "seat": 1,
                    "name": "sonieta1991",
                    "stack": 6.34
                },
                {
                    "seat": 2,
                    "name": "alfonsoterrible",
                    "stack": 4.89
                },
                {
                    "seat": 3,
                    "name": "muelliman1",
                    "stack": 7.45
                },
                {
                    "seat": 4,
                    "name": "Nicoromero87",
                    "stack": 6.0
                },
                {
                    "seat": 5,
                    "name": "Tamaragn",
                    "stack": 3.5
                },
                {
                    "seat": 6,
                    "name": "Fiel.8504200",
                    "stack": 4.98
                }
            ],
            "hero_cards": [
                "Kh",
                "9d"
            ],
            "hero_name": "Nicoromero87",
            "hero_seat": 4,
            "actions": [
                {
                    "phase": "PRE-FLOP",
                    "player": "alfonsoterrible",
                    "action": "small_blind",
                    "amount": 0.02,
                    "cards": []
                },
                {
                    "phase": "PRE-FLOP",
                    "player": "muelliman1",
                    "action": "big_blind",
                    "amount": 0.05,
                    "cards": []
                },
                {
                    "phase": "PRE-FLOP",
                    "player": "Nicoromero87",
                    "action": "fold",
                    "amount": None,
                    "cards": []
                },
                {
                    "phase": "PRE-FLOP",
                    "player": "Tamaragn",
                    "action": "fold",
                    "amount": None,
                    "cards": []
                },
                {
                    "phase": "PRE-FLOP",
                    "player": "Fiel.8504200",
                    "action": "raise",
                    "amount": 0.11,
                    "cards": []
                },
                {
                    "phase": "PRE-FLOP",
                    "player": "sonieta1991",
                    "action": "fold",
                    "amount": None,
                    "cards": []
                },
                {
                    "phase": "PRE-FLOP",
                    "player": "alfonsoterrible",
                    "action": "fold",
                    "amount": None,
                    "cards": []
                },
                {
                    "phase": "PRE-FLOP",
                    "player": "muelliman1",
                    "action": "fold",
                    "amount": None,
                    "cards": []
                }
            ],
            "summary": {
                "player_actions": [
                    {
                        "seat": 1,
                        "name": "sonieta1991",
                        "details": "se retiró antes del Flop (no apostó)"
                    },
                    {
                        "seat": 2,
                        "name": "alfonsoterrible",
                        "details": "se retiró antes del Flop"
                    },
                    {
                        "seat": 3,
                        "name": "muelliman1",
                        "details": "se retiró antes del Flop"
                    },
                    {
                        "seat": 4,
                        "name": "Nicoromero87",
                        "details": "se retiró antes del Flop (no apostó)"
                    },
                    {
                        "seat": 5,
                        "name": "Tamaragn",
                        "details": "se retiró antes del Flop (no apostó)"
                    },
                    {
                        "seat": 6,
                        "name": "Fiel.8504200",
                        "details": "recaudó (0.12 €)"
                    }
                ],
                "pot": 0.12,
                "rake": 0.0,
                "currency": "€",
                "winner": {
                    "name": "Fiel.8504200",
                    "seat": 6,
                    "cards": [],
                    "amount": 0.12,
                    "currency": "€"
                },
                "looser": None,
                "community_cards": [],
                "showdown": False,
                "last_phase_hero_folded": "PRE_FLOP",
                "hero_seat": 4,
                "pot_type": "OPEN_RAISED"
            },
            "showdown": None,
            "finish_before_showdown": [
                {
                    "player": "Fiel.8504200",
                    "action": "uncalled_bet_return",
                    "amount": 0.06
                },
                {
                    "player": "Fiel.8504200",
                    "action": "wins_pot",
                    "amount": 0.12
                }
            ]
        }
    ]
def stats_generator_test():
    expected_stats = {
        "sonieta1991": {
            "HANDS": 2,
            "FOLD": 2,
            "LIMP": 0,
            "OR": 0,
            "ROL": 0,
            "3BET": 0,
            "SQUEEZE": 0,
            "4BET": 0,
            "CALL_TO_OR": 0,
            "CALL_TO_ROL": 0,
            "CALL_TO_3BET": 0,
            "CALL_TO_SQUEEZE": 0,
            "CALL_TO_4BET": 0,
            "FOLD_TO_3BET": 0,
            "FOLD_TO_SQUEEZE": 0,
            "FOLD_TO_4BET": 0,
            "3BET_OPP": 1,
            "VPIP": 0.0,
            "PFR": 0.0,
            "3BET%": 0.0
        },
        "Nicoromero87": {
            "HANDS": 2,
            "FOLD": 2,
            "LIMP": 0,
            "OR": 0,
            "ROL": 0,
            "3BET": 0,
            "SQUEEZE": 0,
            "4BET": 0,
            "CALL_TO_OR": 0,
            "CALL_TO_ROL": 0,
            "CALL_TO_3BET": 0,
            "CALL_TO_SQUEEZE": 0,
            "CALL_TO_4BET": 0,
            "FOLD_TO_3BET": 0,
            "FOLD_TO_SQUEEZE": 0,
            "FOLD_TO_4BET": 0,
            "3BET_OPP": 0,
            "VPIP": 0.0,
            "PFR": 0.0,
            "3BET%": 0.0
        },
        "Ermufa": {
            "HANDS": 1,
            "FOLD": 1,
            "LIMP": 0,
            "OR": 0,
            "ROL": 0,
            "3BET": 0,
            "SQUEEZE": 0,
            "4BET": 0,
            "CALL_TO_OR": 0,
            "CALL_TO_ROL": 0,
            "CALL_TO_3BET": 0,
            "CALL_TO_SQUEEZE": 0,
            "CALL_TO_4BET": 0,
            "FOLD_TO_3BET": 0,
            "FOLD_TO_SQUEEZE": 0,
            "FOLD_TO_4BET": 0,
            "3BET_OPP": 0,
            "VPIP": 0.0,
            "PFR": 0.0,
            "3BET%": 0.0
        },
        "alfonsoterrible": {
            "HANDS": 2,
            "FOLD": 2,
            "LIMP": 0,
            "OR": 0,
            "ROL": 0,
            "3BET": 0,
            "SQUEEZE": 0,
            "4BET": 0,
            "CALL_TO_OR": 0,
            "CALL_TO_ROL": 0,
            "CALL_TO_3BET": 0,
            "CALL_TO_SQUEEZE": 0,
            "CALL_TO_4BET": 0,
            "FOLD_TO_3BET": 0,
            "FOLD_TO_SQUEEZE": 0,
            "FOLD_TO_4BET": 0,
            "3BET_OPP": 1,
            "VPIP": 0.0,
            "PFR": 0.0,
            "3BET%": 0.0
        },
        "Tamaragn": {
            "HANDS": 1,
            "FOLD": 1,
            "LIMP": 0,
            "OR": 0,
            "ROL": 0,
            "3BET": 0,
            "SQUEEZE": 0,
            "4BET": 0,
            "CALL_TO_OR": 0,
            "CALL_TO_ROL": 0,
            "CALL_TO_3BET": 0,
            "CALL_TO_SQUEEZE": 0,
            "CALL_TO_4BET": 0,
            "FOLD_TO_3BET": 0,
            "FOLD_TO_SQUEEZE": 0,
            "FOLD_TO_4BET": 0,
            "3BET_OPP": 0,
            "VPIP": 0.0,
            "PFR": 0.0,
            "3BET%": 0.0
        },
        "Fiel.8504200": {
            "HANDS": 1,
            "FOLD": 0,
            "LIMP": 0,
            "OR": 1,
            "ROL": 0,
            "3BET": 0,
            "SQUEEZE": 0,
            "4BET": 0,
            "CALL_TO_OR": 0,
            "CALL_TO_ROL": 0,
            "CALL_TO_3BET": 0,
            "CALL_TO_SQUEEZE": 0,
            "CALL_TO_4BET": 0,
            "FOLD_TO_3BET": 0,
            "FOLD_TO_SQUEEZE": 0,
            "FOLD_TO_4BET": 0,
            "3BET_OPP": 0,
            "VPIP": 100.0,
            "PFR": 100.0,
            "3BET%": 0.0
        },
        "muelliman1": {
            "3BET_OPP": 1,
            "FOLD": 1,
            "HANDS": 1,
            "OR": 0,
            "ROL": 0,
            "3BET": 0,
            "SQUEEZE": 0,
            "4BET": 0,
            "VPIP": 0.0,
            "PFR": 0.0,
            "3BET%": 0.0
        }
    }
    stats_generator = GameStateHandler(mock_hands)
    stats = stats_generator.execute()

    for _, (player_name, value) in enumerate(expected_stats.items()):
        assert stats[player_name]["HANDS"] == value["HANDS"]
        assert stats[player_name]["VPIP"] == value["VPIP"]
        assert stats[player_name]["PFR"] == value["PFR"]
        assert stats[player_name]["3BET%"] == value["3BET%"]
        
    