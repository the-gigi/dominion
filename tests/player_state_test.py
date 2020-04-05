import random

from card_stack import CardStack
from game import Game
from cards import *
from player_state import PlayerState

import unittest


class TestPlayerState(unittest.TestCase):
    def test_initialize_draw_deck(self):
        """
        ✔ Create new player state
        Check if the player has exactly 7 coppers and 3 estates in their Draw Deck
        Check if the deck are shuffled
        """
        player_state = PlayerState('Sara')
        expected_deck = CardStack([Copper()] * 7 + [Estate()] * 3)
        self.assertEqual(player_state.draw_deck, expected_deck)


if __name__ == '__main__':
    unittest.main()

randominteger = 0

print(random.randominteger(1,100))