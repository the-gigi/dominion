from game_engine import GameEngine
from cards import *
from player_state import PlayerState

import unittest


class TestGameEngine(unittest.TestCase):
    def test_init(self):
        pass

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
