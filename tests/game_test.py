import card_util
from card_util import get_card_types, setup_piles
from game import Game
from cards import *
from player_state import PlayerState
from card_stack import *

import unittest


class GameTest(unittest.TestCase):
    def setUp(self):
        card_types = get_card_types()[:10]
        self.names = ['tester1', 'tester2', 'tester3', 'tester4']
        piles = setup_piles(card_types, len(self.names))

        player_states = [PlayerState(n, piles) for n in self.names]
        self.game = Game(piles, player_states)

    def test_init(self):
        pass

    def test_is_over(self):
        # new game, game not over
        self.assertFalse(self.game.is_over)

        # provinces are empty, game over
        self.game.piles[Province] = 0
        self.assertTrue(self.game.is_over)

        # 2 empty piles, game not over
        self.game.piles[Province] = 1
        self.game.piles[Silver] = 0
        self.game.piles[Copper] = 0
        self.assertFalse(self.game.is_over)

        # 3 empty piles, game over
        self.game.piles[Curse] = 0
        self.assertTrue(self.game.is_over)

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
        # Player has starting deck (3 Estates)
        player_state = self.game.player_states[0]
        point_count = self.game.count_player_points(player_state)
        self.assertEqual(point_count, 3)

        # Player has Province, Duchy, and Estate
        player_state.hand = [Province()]
        player_state.draw_deck.cards = [Duchy()]
        player_state.discard_pile.cards = [Estate()]
        point_count = self.game.count_player_points(player_state)
        self.assertEqual(point_count, 10)

        # Player only has Provinces
        player_state.hand = [Province(), Province()]
        player_state.draw_deck.cards = [Province()]
        player_state.discard_pile.cards = [Province()]
        point_count = self.game.count_player_points(player_state)
        self.assertEqual(point_count, 24)

        # Player only has Duchys
        player_state.hand = [Duchy(), Duchy(), Duchy()]
        player_state.draw_deck.cards = []
        player_state.discard_pile.cards = [Duchy()]
        point_count = self.game.count_player_points(player_state)
        self.assertEqual(point_count, 12)

        # Player only has Estates
        player_state.hand = []
        player_state.draw_deck.cards = []
        player_state.discard_pile.cards = [Estate()]
        point_count = self.game.count_player_points(player_state)
        self.assertEqual(point_count, 1)

        # Player has no Victory Points
        player_state.hand = []
        player_state.draw_deck.cards = []
        player_state.discard_pile.cards = []
        point_count = self.game.count_player_points(player_state)
        self.assertEqual(point_count, 0)

        # Player has just curses
        player_state.hand = [Curse()]
        player_state.draw_deck.cards = [Curse()] * 4
        player_state.discard_pile.cards = []
        point_count = self.game.count_player_points(player_state)
        self.assertEqual(point_count, -5)

        # Player has Curses, Provinces, Duchys, and Estates
        player_state.hand = [Curse(), Province(), Duchy()]
        player_state.draw_deck.cards = [Curse()] * 4
        player_state.discard_pile.cards = [Estate()] * 10
        point_count = self.game.count_player_points(player_state)
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
        # Player has starting deck (7 Coppers)
        player_state = self.game.player_states[0]
        money_count = self.game.count_player_money(player_state)
        self.assertEqual(money_count, 7)

        # Player has Gold, Silver, and Copper
        player_state.hand = [Gold()]
        player_state.draw_deck.cards = [Silver()]
        player_state.discard_pile.cards = [Copper()]
        money_count = self.game.count_player_money(player_state)
        self.assertEqual(money_count, 6)

        # Player only has Gold
        player_state.hand = [Gold()]
        player_state.draw_deck.cards = [Gold()]
        player_state.discard_pile.cards = [Gold()]
        money_count = self.game.count_player_money(player_state)
        self.assertEqual(money_count, 9)

        # Player only has Silver
        player_state.hand = [Silver()]
        player_state.draw_deck.cards = [Silver()]
        player_state.discard_pile.cards = [Silver()]
        money_count = self.game.count_player_money(player_state)
        self.assertEqual(money_count, 6)

        # Player only has Copper
        player_state.hand = [Copper()]
        player_state.draw_deck.cards = [Copper()]
        player_state.discard_pile.cards = [Copper()]
        money_count = self.game.count_player_money(player_state)
        self.assertEqual(money_count, 3)

        # Player has no money
        player_state.hand = []
        player_state.draw_deck.cards = []
        player_state.discard_pile.cards = []
        money_count = self.game.count_player_money(player_state)
        self.assertEqual(money_count, 0)

    def test_verify_action(self):
        """
        card not in hand, card not an action, no actions (0, 0, 0)
        card not in hand, card not an action, has actions (0, 0, 1)
        card not in hand, card is an action, has actions (0, 1, 1)
        card not in hand, card is an action, no actions (0, 1, 0)
        card in hand, card not an action, has actions (1, 0, 1)
        card in hand, card not an action, no actions (1, 0, 0)
        card in hand, card is an action, has actions (1, 1, 1)
        card in hand, card is an action, no actions (1, 1, 0)

        :return:
        """
        player_state = self.game.player_state

        # 0, 0, 0
        test_card = Copper()
        player_state.hand = []
        player_state.actions = 0
        is_verified = self.game._verify_action(test_card)
        self.assertFalse(is_verified)

        # 0, 0, 1
        test_card = Copper()
        player_state.hand = []
        player_state.actions = 1
        is_verified = self.game._verify_action(test_card)
        self.assertFalse(is_verified)

        # 0, 1, 1
        test_card = Moat()
        player_state.hand = []
        player_state.actions = 1
        is_verified = self.game._verify_action(test_card)
        self.assertFalse(is_verified)

        # 0, 1, 0
        test_card = Moat()
        player_state.hand = []
        player_state.actions = 0
        is_verified = self.game._verify_action(test_card)
        self.assertFalse(is_verified)

        # 1, 0, 1
        test_card = Copper()
        player_state.hand = [test_card]
        player_state.actions = 1
        is_verified = self.game._verify_action(test_card)
        self.assertFalse(is_verified)

        # 1, 0, 0
        test_card = Copper()
        player_state.hand = [test_card]
        player_state.actions = 0
        is_verified = self.game._verify_action(test_card)
        self.assertFalse(is_verified)

        # 1, 1, 1
        test_card = Moat()
        player_state.hand = [test_card]
        player_state.actions = 1
        is_verified = self.game._verify_action(test_card)
        self.assertTrue(is_verified)

        # 1, 1, 0
        test_card = Moat()
        player_state.hand = [test_card]
        player_state.actions = 0
        is_verified = self.game._verify_action(test_card)
        self.assertFalse(is_verified)

    def test_verify_buy(self):
        """
        has enough money, has buys (1, 1)
        has enough money, no buys (1, 0)
        not enough money, has buys (0, 1)
        not enough money, no buys (0, 0)
        :return:
        """
        player_state = self.game.player_state

        # 1, 1
        player_state.hand = [Silver(), Copper(), Gold()]
        player_state.buys = 1
        is_verified = self.game._verify_buy(Gold())
        self.assertTrue(is_verified)

        # 1, 0
        player_state.hand = [Gold()]
        player_state.buys = 0
        is_verified = self.game._verify_buy(Moat())
        self.assertFalse(is_verified)

        # 0, 1
        player_state.hand = [Copper()]
        player_state.buys = 1
        is_verified = self.game._verify_buy(Moat())
        self.assertFalse(is_verified)

        # 0, 0
        player_state.hand = [Copper()]
        player_state.buys = 0
        is_verified = self.game._verify_buy(Moat())
        self.assertFalse(is_verified)

    def test_find_winners(self):
        """
        Everyone has an equal amount of points
        A couple people have an equal amount of points
        One person has the most points

        Tie-breaker
        Everyone has an equal amount of coins
        A couple people have the highest amount of coins
        One person has the most coins
        :return:
        """
        # equal points
        winners = self.game.find_winners()
        expected = self.names
        self.assertEqual(winners, expected)

        # pair with equal points
        self.game.player_states[0].hand = []
        self.game.player_states[1].hand = []
        self.game.player_states[2].hand = [Estate()]
        self.game.player_states[3].hand = [Estate()]
        self.game.player_states[0].discard_pile = CardStack()
        self.game.player_states[0].draw_deck = CardStack()
        self.game.player_states[1].discard_pile = CardStack()
        self.game.player_states[1].draw_deck = CardStack()
        self.game.player_states[2].discard_pile = CardStack()
        self.game.player_states[2].draw_deck = CardStack()
        self.game.player_states[3].discard_pile = CardStack()
        self.game.player_states[3].draw_deck = CardStack()
        winners = self.game.find_winners()
        expected = ['tester3', 'tester4']
        self.assertEqual(winners, expected)

        # one winner
        self.game.player_states[0].hand = [Duchy(), Province()]
        self.game.player_states[1].hand = []
        self.game.player_states[2].hand = []
        self.game.player_states[3].hand = []
        self.game.player_states[0].discard_pile = CardStack()
        self.game.player_states[0].draw_deck = CardStack()
        self.game.player_states[1].discard_pile = CardStack()
        self.game.player_states[1].draw_deck = CardStack()
        self.game.player_states[2].discard_pile = CardStack()
        self.game.player_states[2].draw_deck = CardStack()
        self.game.player_states[3].discard_pile = CardStack()
        self.game.player_states[3].draw_deck = CardStack()
        winners = self.game.find_winners()
        expected = ['tester1']
        self.assertEqual(winners, expected)

        # TIE-BREAKER
        # equal coins
        self.game.player_states[0].hand = [Copper()]
        self.game.player_states[1].hand = [Copper()]
        self.game.player_states[2].hand = [Copper()]
        self.game.player_states[3].hand = [Copper()]
        self.game.player_states[0].discard_pile = CardStack()
        self.game.player_states[0].draw_deck = CardStack()
        self.game.player_states[1].discard_pile = CardStack()
        self.game.player_states[1].draw_deck = CardStack()
        self.game.player_states[2].discard_pile = CardStack()
        self.game.player_states[2].draw_deck = CardStack()
        self.game.player_states[3].discard_pile = CardStack()
        self.game.player_states[3].draw_deck = CardStack()
        winners = self.game.find_winners()
        expected = ['tester1', 'tester2', 'tester3', 'tester4']
        self.assertEqual(winners, expected)

        #pair with equal coins
        self.game.player_states[0].hand = []
        self.game.player_states[1].hand = []
        self.game.player_states[2].hand = [Silver()]
        self.game.player_states[3].hand = [Silver()]
        self.game.player_states[0].discard_pile = CardStack()
        self.game.player_states[0].draw_deck = CardStack()
        self.game.player_states[1].discard_pile = CardStack()
        self.game.player_states[1].draw_deck = CardStack()
        self.game.player_states[2].discard_pile = CardStack()
        self.game.player_states[2].draw_deck = CardStack()
        self.game.player_states[3].discard_pile = CardStack()
        self.game.player_states[3].draw_deck = CardStack()
        winners = self.game.find_winners()
        expected = ['tester3', 'tester4']
        self.assertEqual(winners, expected)

        # one winner
        self.game.player_states[0].hand = []
        self.game.player_states[1].hand = [Gold()]
        self.game.player_states[2].hand = []
        self.game.player_states[3].hand = []
        self.game.player_states[0].discard_pile = CardStack()
        self.game.player_states[0].draw_deck = CardStack()
        self.game.player_states[1].discard_pile = CardStack()
        self.game.player_states[1].draw_deck = CardStack()
        self.game.player_states[2].discard_pile = CardStack()
        self.game.player_states[2].draw_deck = CardStack()
        self.game.player_states[3].discard_pile = CardStack()
        self.game.player_states[3].draw_deck = CardStack()
        winners = self.game.find_winners()
        expected = ['tester2']
        self.assertEqual(winners, expected)

    def test_play_action_card(self):
        """
        create a game with a player with an action card in their hand
        call play_action_card()
        check if the card got moved from the hand to the play area
        """
        moat = Moat()
        self.game.player_state.hand = [moat]
        ok = self.game.play_action_card(moat)
        self.assertTrue(ok)
        self.assertNotEqual(self.game.player_state.hand, [moat])
        self.assertEqual(self.game.player_state.play_area, [moat])

        bureaucrat = Bureaucrat()
        self.game.player_state.play_area = []
        self.game.player_state.hand = [bureaucrat]
        ok = self.game.play_action_card(moat)
        self.assertFalse(ok)
        self.assertEqual(self.game.player_state.hand, [bureaucrat])
        self.assertEqual(self.game.player_state.play_area, [])

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
