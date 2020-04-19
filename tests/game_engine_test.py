from card_util import get_card_types
from computer_players.simpleton import Simpleton
from cards import *
from game_factory import create_game_engine

import unittest


class TestGameEngine(unittest.TestCase):
    def setUp(self):
        card_types = get_card_types()[:10]
        players_info = players_info = dict(
            Gus=Simpleton,
            Sara=Simpleton,
            Beaver=Simpleton,
            Igig=Simpleton
        )
        self.game_engine = create_game_engine(card_types, players_info)

    def test_init(self):
        pass

    def test_game_over(self):
        # new game, game not over
        self.assertFalse(self.game_engine.game_over)

        # provinces are empty, game over
        self.game_engine.game_object.piles[Province] = 0
        game_over_true_province = self.game_engine.game_over
        self.assertTrue(self.game_engine.game_over)

        # 2 empty piles, game not over
        self.game_engine.game_object.piles[Province] = 1
        self.game_engine.game_object.piles[Silver] = 0
        self.game_engine.game_object.piles[Copper] = 0
        self.assertFalse(self.game_engine.game_over)

        # 3 empty piles, game over
        self.game_engine.game_object.piles[Curse] = 0
        self.assertTrue(self.game_engine.game_over)

    def test_count_player_points(self):
        """ """
        #self.fail()

    def test_count_player_money(self):
        """ """
        # self.fail()

    def test_find_winner(self):
        """"""
        #self.fail()

    def test_is_pile_empty(self):
        """"""
        #self.fail()

    def test_get_active_player(self):
        """"""
        #self.fail()

    def test_finish_turn(self):
        """"""
        # self.fail()

    def test_run(self):
        """"""
        # self.fail()


if __name__ == '__main__':
    unittest.main()
