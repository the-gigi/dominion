from game_engine import GameEngine
from cards import *
from player_state import PlayerState

import unittest


class TestGameEngine(unittest.TestCase):
    def test_init(self):
        names = ['Gus', 'Sara', 'Beaver', 'Igig']
        players = [PlayerState(name) for name in names]
        card_types = [Copper, Silver, Gold, Estate, Duchy, Province, Curse]
        game = None
        game_engine_4p = GameEngine(game, players, card_types)
        game_engine_3p = GameEngine(game, players[:3], card_types)
        game_engine_2p = GameEngine(game, players[:2], card_types)

        expected_players_4p = players
        expected_active_player = 0
        expected_piles_4p = {Copper: 32, Silver: 40, Gold: 30, Estate: 12, Duchy: 12, Province: 12, Curse: 30}

        expected_players_3p = players[:3]
        expected_piles_3p = {Copper: 39, Silver: 40, Gold: 30, Estate: 12, Duchy: 12, Province: 12, Curse: 20}

        expected_players_2p = players[:2]
        expected_piles_2p = {Copper: 46, Silver: 40, Gold: 30, Estate: 8, Duchy: 8, Province: 8, Curse: 10}

        self.assertEqual(expected_players_4p, game_engine_4p.players)
        self.assertEqual(expected_active_player, game_engine_4p.active_player_index)
        self.assertEqual(expected_piles_4p, game_engine_4p.piles)

        self.assertEqual(expected_players_3p, game_engine_3p.players)
        self.assertEqual(expected_active_player, game_engine_3p.active_player_index)
        self.assertEqual(expected_piles_3p, game_engine_3p.piles)

        self.assertEqual(expected_players_2p, game_engine_2p.players)
        self.assertEqual(expected_active_player, game_engine_2p.active_player_index)
        self.assertEqual(expected_piles_2p, game_engine_2p.piles)

    def test_game_over(self):
        names = ['Gus', 'Sara', 'Beaver', 'Igig']
        players = [PlayerState(name) for name in names]
        card_types = [Copper, Silver, Gold, Estate, Duchy, Province, Curse]
        game = None
        # new game, game not over
        game_engine = GameEngine(game, players, card_types)
        self.assertFalse(game_engine.game_over)

        # provinces are empty, game over
        game_engine.piles[Province] = 0
        game_over_true_province = game_engine.game_over
        self.assertTrue(game_engine.game_over)

        # 2 empty piles, game not over
        game_engine.piles[Province] = 1
        game_engine.piles[Silver] = 0
        game_engine.piles[Copper] = 0
        self.assertFalse(game_engine.game_over)

        # 3 empty piles, game over
        game_engine.piles[Curse] = 0
        game_over_true_other = game_engine.game_over
        self.assertTrue(game_engine.game_over)

    def test_count_player_points(self):
        self.fail()

    def test_count_player_money(self):
        self.fail()

    def test_find_winner(self):
        self.fail()

    def test_is_pile_empty(self):
        self.fail()

    def test_get_active_player(self):
        self.fail()

    def test_finish_turn(self):
        self.fail()

    def test_run(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()
