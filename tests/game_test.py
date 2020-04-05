from game import Game
from cards import *
from player_state import PlayerState

import unittest


class TestGame(unittest.TestCase):
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
        """
        create player with some victory points
        call the count_player_points()
        check we got the correct amount

        test cases:
        - player with just provinces
        - player with just duchys
        - player with just estates
        - player with all of the above
        - player with no points at all

        :return:
        """
        names = ['Igig']
        game = Game(names)

        # Player has Province, Duchy, and Estate
        player_state = game.state.player_states[0]
        player_state.hand.append(Province())
        player_state.draw_deck.cards.append(Duchy())
        player_state.discard_pile.cards.append(Estate())
        point_count = game.count_player_points(player_state)
        self.assertEqual(point_count, 10)

        # Player only has Provinces
        player_state.hand = [Province(), Province()]
        player_state.draw_deck.cards = [Province()]
        player_state.discard_pile.cards = [Province()]
        point_count = game.count_player_points(player_state)
        self.assertEqual(point_count, 24)

        # Player only has Duchys
        player_state.hand = [Duchy(), Duchy(), Duchy()]
        player_state.draw_deck.cards = []
        player_state.discard_pile.cards = [Duchy()]
        point_count = game.count_player_points(player_state)
        self.assertEqual(point_count, 12)

        # Player only has Estates
        player_state.hand = []
        player_state.draw_deck.cards = []
        player_state.discard_pile.cards = [Estate()]
        point_count = game.count_player_points(player_state)
        self.assertEqual(point_count, 1)

        # Player has no Victory Points
        player_state.hand = []
        player_state.draw_deck.cards = []
        player_state.discard_pile.cards = []
        point_count = game.count_player_points(player_state)
        self.assertEqual(point_count, 0)

        # Player has just curses
        player_state.hand = [Curse()]
        player_state.draw_deck.cards = [Curse()] * 4
        player_state.discard_pile.cards = []
        point_count = game.count_player_points(player_state)
        self.assertEqual(point_count, -5)

        # Player has Curses, Provinces, Duchys, and Estates
        player_state.hand = [Curse(), Province(), Duchy()]
        player_state.draw_deck.cards = [Curse()] * 4
        player_state.discard_pile.cards = [Estate()] * 10
        point_count = game.count_player_points(player_state)
        self.assertEqual(point_count, 14)

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
