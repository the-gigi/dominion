from dominion.card_stack import CardStack
from dominion.card_util import *
from dominion.cards import *
from dominion.player_state import PlayerState

import unittest


class TestPlayerState(unittest.TestCase):
    def setUp(self):
        card_types = get_card_types()
        piles = setup_piles(card_types, 4)
        self.player_state = PlayerState('tester1', piles)

    def test_initialize_draw_deck(self):
        """
        √ Create new player state
        √ Check if the player has exactly 7 coppers and 3 estates in their Draw Deck
        """

        self.player_state.draw_deck.cards += self.player_state.hand
        self.player_state.hand = []

        num_coppers = sum(1 if type(c) == Copper else 0 for c in self.player_state.draw_deck.cards)
        num_estates = sum(1 if type(c) == Estate else 0 for c in self.player_state.draw_deck.cards)

        self.assertEqual(num_coppers, 7)
        self.assertEqual(num_estates, 3)

    def test_draw_cards(self):
        """
        draw 0 cards
        draw 1 card with no cards in deck or discard
        draw multiple cards with no cards in deck or discard

        draw 1 card with no cards in deck and 1 card in discard
        draw multiple cards with no cards in deck and 1 card in discard

        draw 1 card with 1 card in deck and multiple cards in discard
        draw multiple cards with 1 card in deck and multiple cards in discard

        draw 1 card with multiple cards in deck
        draw multiple cards with multiple cards in deck
        """

        # draw 0 cards
        copper = Copper()
        silver = Silver()
        gold = Gold()
        estate = Estate()
        self.player_state.hand = [copper]
        self.player_state.draw_deck.cards = [silver]
        self.player_state.discard_pile.cards = []
        self.player_state.draw_cards(0)
        expected = [copper]
        self.assertEqual(self.player_state.hand, expected)
        self.assertEqual(self.player_state.draw_deck.cards, [silver])

        # draw 1 card with no cards in deck or discard
        self.player_state.hand = [copper]
        self.player_state.draw_deck.cards = []
        expected = [copper]
        self.player_state.draw_cards(1)
        self.assertEqual(self.player_state.hand, expected)

        expected = [copper]
        self.player_state.draw_cards(3)
        self.assertEqual(self.player_state.hand, expected)

        # draw 1 card with no cards in deck and 1 card in discard
        self.player_state.hand = [copper]
        self.player_state.draw_deck.cards = []
        self.player_state.discard_pile.cards = [silver]
        self.player_state.draw_cards(1)
        expected = [copper, silver]
        self.assertEqual(self.player_state.hand, expected)

        # draw multiple cards with no cards in deck and 1 card in discard
        self.player_state.hand = [copper]
        self.player_state.draw_deck.cards = []
        self.player_state.discard_pile.cards = [silver]
        expected = [copper, silver]
        self.player_state.draw_cards(3)
        self.assertEqual(self.player_state.hand, expected)

        # draw 1 card with 1 card in deck and multiple cards in discard
        self.player_state.hand = [copper]
        self.player_state.draw_deck.cards = [silver]
        self.player_state.discard_pile.cards = [gold, estate]
        self.player_state.draw_cards(1)
        expected = [copper, silver]
        self.assertEqual(self.player_state.hand, expected)

        # draw multiple cards with 1 card in deck and multiple cards in discard
        self.player_state.hand = [copper]
        self.player_state.draw_deck.cards = [silver]
        self.player_state.draw_cards(3)
        expected = as_dict([copper, silver, gold, estate])
        self.assertEqual(as_dict(self.player_state.hand), expected)

        # draw 1 card with multiple cards in deck
        self.player_state.hand = [copper]
        self.player_state.draw_deck.cards = [silver, gold, estate]
        self.player_state.discard_pile.cards = []
        self.player_state.draw_cards(1)
        expected = [copper, silver]
        self.assertEqual(self.player_state.hand, expected)

        # draw multiple cards with multiple cards in deck
        self.player_state.hand = [copper]
        self.player_state.draw_deck.cards = [silver, gold, estate]
        self.player_state.discard_pile.cards = []
        self.player_state.draw_cards(3)
        expected = [copper, silver, gold, estate]
        self.assertEqual(self.player_state.hand, expected)


if __name__ == '__main__':
    unittest.main()
