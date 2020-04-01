from game_engine import GameEngine
from cards import Copper, Estate
from player import Player

import unittest


class TestGameEngine(unittest.TestCase):
    def test_init(self):
        names = ['Gus', 'Sara', 'Beaver']
        players = [Player(name) for name in names]
        card_types = [Copper, Estate]
        game_engine = GameEngine(players, card_types)

        expected_players = players
        expected_active_player = 0
        expected_piles = {Copper: 39, Estate: 12}
        self.assertEqual(expected_players, game_engine.players)
        self.assertEqual(expected_active_player, game_engine.active_player)
        self.assertEqual(expected_piles, game_engine.piles)


    def test_game_over(self):
        pass

    def test_count_player_points(self, player):
        pass

    def test_count_player_money(self, player):
        pass

    def test_find_winner(self, players):
        pass

    def test_is_pile_empty(self, card_type):
        pass

    def test_get_active_player(self):
        pass

    def test_finish_turn(self):
        pass

    def test_run(self):
        pass

if __name__ == '__main__':
    unittest.main()
