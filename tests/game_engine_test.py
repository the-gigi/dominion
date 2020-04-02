from game_engine import GameEngine
from cards import Copper, Estate
from player_state import Player

import unittest


class TestGameEngine(unittest.TestCase):
    def test_init(self):
        names = ['Gus', 'Sara', 'Beaver']
        players = [Player(name) for name in names]
        card_types = [Copper, Estate]
        game = None
        game_engine = GameEngine(game, players, card_types)

        expected_players = players
        expected_active_player = 0
        expected_piles = {Copper: 39, Estate: 12}
        self.assertEqual(expected_players, game_engine.players)
        self.assertEqual(expected_active_player, game_engine.active_player_index)
        self.assertEqual(expected_piles, game_engine.piles)

    def test_game_over(self):
        self.fail()

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
