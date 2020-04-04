from game import Game
from cards import *
from player_state import PlayerState

import unittest


class TestGameEngine(unittest.TestCase):
    def test_init(self):
        pass

    def test_is_over(self):
        names = ['Gus', 'Sara', 'Beaver', 'Igig']
        # new game, game not over
        game = Game(names)
        self.assertFalse(game.is_over)

        # provinces are empty, game over
        game.piles[Province] = 0
        self.assertTrue(game.is_over)

        # 2 empty piles, game not over
        game.piles[Province] = 1
        game.piles[Silver] = 0
        game.piles[Copper] = 0
        self.assertFalse(game.is_over)

        # 3 empty piles, game over
        game.piles[Curse] = 0
        self.assertTrue(game.is_over)

    def test_count_player_points(self):
        self.fail()

    def test_count_player_money(self):
        """
        create player with some moneys
        call the count_player_money()
        check we got the correct amount
        
        test cases:
        - player with just gold
        - player with just silver
        - player with just copper
        - player with all of the above 
        - player with no money at all

        :return:
        """
        names = ['Gus']
        game = Game(names)

        # Player has Gold, Silver, and Copper
        player_state = game.state.player_states[0]
        player_state.hand.append(Gold())
        player_state.draw_deck.cards.append(Silver())
        player_state.discard_pile.cards.append(Copper())
        money_count = game.count_player_money(player_state)
        self.assertEqual(money_count, 6)

        # Player only has Gold
        player_state.hand = [Gold()]
        player_state.draw_deck.cards = [Gold()]
        player_state.discard_pile.cards = [Gold()]
        money_count = game.count_player_money(player_state)
        self.assertEqual(money_count, 9)

        # Player only has Silver
        player_state.hand = [Silver()]
        player_state.draw_deck.cards = [Silver()]
        player_state.discard_pile.cards = [Silver()]
        money_count = game.count_player_money(player_state)
        self.assertEqual(money_count, 6)

        # Player only has Copper
        player_state.hand = [Copper()]
        player_state.draw_deck.cards = [Copper()]
        player_state.discard_pile.cards = [Copper()]
        money_count = game.count_player_money(player_state)
        self.assertEqual(money_count, 3)

        # Player has no money
        player_state.hand = []
        player_state.draw_deck.cards = []
        player_state.discard_pile.cards = []
        money_count = game.count_player_money(player_state)
        self.assertEqual(money_count, 0)

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
